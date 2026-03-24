"""Thick BaseAgent with schema validation and auto-enrichment."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import perf_counter, sleep
from typing import Any, TypedDict
from uuid import uuid4

from common.infra.db_writer import db_writer
from common.infra.intent_gate import IntentCapsule, IntentGateError, intent_gate
from common.infra.scoped_token import ScopedToken
from common.infra.skill_registry import SKILL_REGISTRY, validate_manifest
from common.infra.task_queue import task_queue
from common.observability.logger import get_logger, log_event


@dataclass(frozen=True)
class AgentManifest:
    """Static identity and routing metadata for an agent."""

    agent_id: str
    model_tier: str = "fast"
    system_prompt: str = ""
    task_name: str = ""
    queue_name: str = ""


class AgentGraphState(TypedDict, total=False):
    input_payload: dict[str, Any]
    prepped: dict[str, Any]
    core_output: dict[str, Any]
    final_output: dict[str, Any]


class SchemaValidationError(Exception):
    """Exception raised when input/output validation fails."""

    pass


def validate_schema(
    data: dict[str, Any],
    schema: dict[str, Any] | None,
    preserve_unknown: bool = True,
) -> dict[str, Any]:
    """
    Lightweight schema validation with type coercion and bounds checking.

    Schema format:
    {"field_name": {"type": "str", "required": True, "default": None, "min": 0, "max": 100}}

    Returns validated and coerced data, raises SchemaValidationError on failure.
    """
    if schema is None:
        return data

    def _coerce_bool(raw: Any) -> bool:
        if isinstance(raw, bool):
            return raw
        if isinstance(raw, int):
            if raw in (0, 1):
                return bool(raw)
            raise TypeError(f"expected bool-compatible int (0/1), got {raw}")
        if isinstance(raw, str):
            lowered = raw.strip().lower()
            if lowered in {"true", "1", "yes", "y", "on"}:
                return True
            if lowered in {"false", "0", "no", "n", "off"}:
                return False
            raise TypeError(f"expected bool-compatible string, got {raw!r}")
        raise TypeError(f"expected bool-compatible value, got {type(raw).__name__}")

    def _validate_value(
        field_name: str,
        value: Any,
        field_spec: dict[str, Any],
    ) -> Any:
        field_type = field_spec.get("type", "str")
        min_val = field_spec.get("min")
        max_val = field_spec.get("max")
        enum_values = field_spec.get("enum")

        try:
            if field_type == "int":
                value = int(value)
            elif field_type == "float":
                value = float(value)
            elif field_type == "str":
                value = str(value)
            elif field_type == "bool":
                value = _coerce_bool(value)
            elif field_type == "dict":
                if not isinstance(value, dict):
                    raise TypeError(f"expected dict, got {type(value).__name__}")
                nested_schema = field_spec.get("schema")
                if nested_schema is not None:
                    nested_preserve_unknown = field_spec.get("preserve_unknown", preserve_unknown)
                    value = validate_schema(value, nested_schema, preserve_unknown=nested_preserve_unknown)
            elif field_type == "list":
                if not isinstance(value, list):
                    raise TypeError(f"expected list, got {type(value).__name__}")
                item_spec = field_spec.get("items")
                if item_spec is not None:
                    validated_items = []
                    for idx, item in enumerate(value):
                        item_name = f"{field_name}[{idx}]"
                        validated_items.append(_validate_value(item_name, item, item_spec))
                    value = validated_items
            else:
                value = value
        except (ValueError, TypeError) as e:
            raise SchemaValidationError(
                f"Field {field_name}: cannot coerce to {field_type}: {e}"
            )

        if enum_values is not None and value not in enum_values:
            raise SchemaValidationError(
                f"Field {field_name}: value {value!r} not in enum {enum_values!r}"
            )

        # Bounds checking (for numeric values only)
        if isinstance(value, (int, float)):
            if min_val is not None and value < min_val:
                raise SchemaValidationError(
                    f"Field {field_name}: value {value} below minimum {min_val}"
                )
            if max_val is not None and value > max_val:
                raise SchemaValidationError(
                    f"Field {field_name}: value {value} above maximum {max_val}"
                )

        return value

    validated: dict[str, Any] = {}
    for field_name, field_spec in schema.items():
        required = field_spec.get("required", False)
        default = field_spec.get("default")

        if field_name not in data:
            if required and default is None:
                raise SchemaValidationError(f"Required field missing: {field_name}")
            validated[field_name] = default
            continue

        validated[field_name] = _validate_value(field_name, data[field_name], field_spec)

    if preserve_unknown:
        for key, value in data.items():
            if key not in validated:
                validated[key] = value

    return validated


class BaseAgent(ABC):
    """
    Thick base class with lifecycle hooks, schema validation, and auto-enrichment.

    Subclasses must define:
    - agent_id, task_name (class vars)
    - core_process() (abstract method - business logic only)

    Subclasses may define:
    - input_schema(), output_schema() (for validation)
    - pre_process(), post_process() (for transformation)
    """

    agent_id: str = "base_agent"
    model_tier: str = "fast"
    system_prompt: str = ""
    task_name: str = ""
    queue_name: str = ""
    result_channel: str = "trip:{trip_id}:events"
    expected_step: int = 1
    permitted_tools: list[str] = []
    permitted_tables: dict[str, list[str]] = {"read": [], "write": []}
    enforce_intent_gate: bool = False
    strict_manifest_validation: bool = False
    enable_langgraph: bool = True
    auto_enrich_output: bool = True
    max_retries: int = 0
    retry_backoff_seconds: float = 0.0
    retry_exceptions: tuple[type[Exception], ...] = (RuntimeError, TimeoutError, ConnectionError)

    def __init__(self) -> None:
        if not self.agent_id.strip():
            raise ValueError("agent_id must not be empty")

        resolved_task_name = self.task_name or f"{self.agent_id}.run"

        self.manifest = AgentManifest(
            agent_id=self.agent_id,
            model_tier=self.model_tier,
            system_prompt=self.system_prompt,
            task_name=resolved_task_name,
            queue_name=self.queue_name,
        )
        self.task_name = resolved_task_name
        if self.strict_manifest_validation:
            validate_manifest(self.agent_id, self.permitted_tools)

        # If subclass didn't define table policy, hydrate from skill registry when present.
        if not self.permitted_tables.get("read") and not self.permitted_tables.get("write"):
            registry_entry = SKILL_REGISTRY.get(self.agent_id, {})
            self.permitted_tables = registry_entry.get("permitted_tables", {"read": [], "write": []})
        db_writer.configure(self.permitted_tables)

        if self.task_name:
            queue = self.queue_name or f"{self.agent_id}_queue"
            task_queue.register(self.task_name, queue, self.run)

        self.execution_trace: list[str] = []
        self.execution_state: dict[str, Any] = {}
        self.logger = get_logger(f"agent.{self.agent_id}")
        self._compiled_graph = self._compile_graph_if_enabled()

    def _parse_capsule(self, data: dict[str, Any]) -> IntentCapsule:
        token_data = data.get("token")
        token: ScopedToken | None = None
        if isinstance(token_data, dict):
            token = ScopedToken(
                token_id=str(token_data.get("token_id", "")),
                agent=str(token_data.get("agent", self.agent_id)),
                expires_at=str(token_data.get("expires_at", "")),
                read_keys=list(token_data.get("read_keys", [])),
                write_keys=list(token_data.get("write_keys", [])),
            )

        return IntentCapsule(
            trip_id=str(data.get("trip_id", "")),
            agent=str(data.get("agent", self.agent_id)),
            priority=int(data.get("priority", 9)),
            step_index=int(data.get("step_index", self.expected_step)),
            issued_by=str(data.get("issued_by", "orchestrator")),
            allowed_inputs=list(data.get("allowed_inputs", [])),
            expected_outputs=list(data.get("expected_outputs", [])),
            permitted_tools=list(data.get("permitted_tools", [])),
            ttl=int(data.get("ttl", 3600)),
            issued_at=str(data.get("issued_at", "")),
            hmac_seal=str(data.get("hmac_seal", "")),
            token=token,
        )

    def _extract_runtime_input(self, input_payload: dict[str, Any]) -> tuple[dict[str, Any], IntentCapsule | None]:
        """Support both legacy direct payloads and secured envelopes with intent capsules."""
        capsule_data = input_payload.get("intent_capsule")
        if isinstance(capsule_data, dict):
            runtime_input = input_payload.get("input_payload")
            if runtime_input is None:
                runtime_input = input_payload.get("payload")
            if not isinstance(runtime_input, dict):
                raise ValueError("input_payload must include a dict 'input_payload' when intent_capsule is provided")
            capsule = self._parse_capsule(capsule_data)
            return runtime_input, capsule
        return input_payload, None

    def input_schema(self) -> dict[str, Any] | None:
        """Return input schema for validation. None = skip validation."""
        return None

    def output_schema(self) -> dict[str, Any] | None:
        """Return output schema for validation. None = skip validation."""
        return None

    def pre_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Hook for input transformation. Called after validation."""
        return input_payload

    @abstractmethod
    def core_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Core business logic. Must implement in subclass."""

    def post_process(self, core_output: dict[str, Any]) -> dict[str, Any]:
        """Hook for output transformation. Called before auto-enrichment."""
        return core_output

    def _auto_enrich_output(self, final_output: dict[str, Any], run_id: str) -> dict[str, Any]:
        """Add agent metadata to output. Can disable with auto_enrich_output=False."""
        if not self.auto_enrich_output:
            return final_output

        return {
            "agent": self.agent_id,
            "task_name": self.task_name,
            "engine": self.execution_state.get("engine"),
            "run_id": run_id,
            **final_output,
        }

    def should_retry(self, exc: Exception, attempt: int) -> bool:
        """Policy hook to decide whether a failed attempt should be retried."""
        return isinstance(exc, self.retry_exceptions) and attempt < self.max_retries

    def on_run_success(self, final_output: dict[str, Any]) -> dict[str, Any]:
        """Lifecycle hook invoked after a successful run and before returning output."""
        return final_output

    def on_run_failure(self, exc: Exception) -> None:
        """Lifecycle hook invoked after retries are exhausted and before raising."""
        return None

    def run(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Execute agent lifecycle: pre_process → core_process → post_process."""
        if not isinstance(input_payload, dict):
            raise ValueError("input_payload must be a dictionary")

        runtime_input, capsule = self._extract_runtime_input(input_payload)
        if self.enforce_intent_gate:
            if capsule is None:
                raise IntentGateError("intent_capsule_required: secure mode requires intent capsule")
            intent_gate.verify(capsule, self.expected_step)

            if capsule.agent and capsule.agent != self.agent_id:
                raise IntentGateError(
                    f"agent_mismatch: capsule agent '{capsule.agent}' does not match '{self.agent_id}'"
                )

            if capsule.permitted_tools:
                undeclared = set(self.permitted_tools) - set(capsule.permitted_tools)
                if undeclared:
                    raise IntentGateError(f"tool_mismatch: local tools not permitted by capsule: {sorted(undeclared)}")

        run_id = str(uuid4())
        started_at = perf_counter()

        # Scope state to single execution
        self.execution_trace = []
        self.execution_state = {}
        self.execution_state["run_id"] = run_id

        log_event(
            self.logger,
            "run_started",
            run_id=run_id,
            agent_id=self.agent_id,
            model_tier=self.model_tier,
            input_keys=sorted(runtime_input.keys()),
        )

        attempt = 0
        while True:
            try:
                # Scope state to single execution attempt.
                self.execution_trace = []
                self.execution_state = {
                    "run_id": run_id,
                    "attempt": attempt + 1,
                }

                if self._compiled_graph is not None:
                    self.execution_state["engine"] = "langgraph"
                    final_output = self._run_langgraph(runtime_input, run_id)
                else:
                    self.execution_state["engine"] = "sequential"
                    final_output = self._run_sequential(runtime_input, run_id)

                final_output = self.on_run_success(final_output)
                duration_ms = round((perf_counter() - started_at) * 1000, 3)
                log_event(
                    self.logger,
                    "run_completed",
                    run_id=run_id,
                    agent_id=self.agent_id,
                    status="ok",
                    duration_ms=duration_ms,
                    attempts_used=attempt + 1,
                )
                return final_output
            except Exception as exc:
                can_retry = self.should_retry(exc, attempt)

                if can_retry:
                    attempt += 1
                    log_event(
                        self.logger,
                        "run_retrying",
                        run_id=run_id,
                        agent_id=self.agent_id,
                        attempt=attempt,
                        max_retries=self.max_retries,
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                    )
                    if self.retry_backoff_seconds > 0:
                        sleep(self.retry_backoff_seconds * attempt)
                    continue

                duration_ms = round((perf_counter() - started_at) * 1000, 3)
                self.on_run_failure(exc)
                log_event(
                    self.logger,
                    "run_failed",
                    run_id=run_id,
                    agent_id=self.agent_id,
                    status="error",
                    duration_ms=duration_ms,
                    error_type=type(exc).__name__,
                    error_message=str(exc),
                    attempts_used=attempt + 1,
                )
                raise

    def _run_sequential(self, input_payload: dict[str, Any], run_id: str) -> dict[str, Any]:
        """Execute lifecycle step-by-step with schema validation."""
        # Validate input
        try:
            validated_input = validate_schema(input_payload, self.input_schema())
        except SchemaValidationError as e:
            log_event(self.logger, "schema_validation_failed", run_id=run_id, error=str(e))
            raise

        self.execution_trace.append("pre_process")
        prepped = self.pre_process(validated_input)
        self.execution_state["prepped"] = prepped
        log_event(self.logger, "step_completed", run_id=run_id, step="pre_process")

        self.execution_trace.append("core_process")
        core_output = self.core_process(prepped)
        self.execution_state["core_output"] = core_output
        log_event(self.logger, "step_completed", run_id=run_id, step="core_process")

        # Validate output
        try:
            validated_output = validate_schema(core_output, self.output_schema())
        except SchemaValidationError as e:
            log_event(self.logger, "schema_validation_failed", run_id=run_id, error=str(e))
            raise

        self.execution_trace.append("post_process")
        final_output = self.post_process(validated_output)
        self.execution_state["final_output"] = final_output
        log_event(self.logger, "step_completed", run_id=run_id, step="post_process")

        enriched_output = self._auto_enrich_output(final_output, run_id)
        return enriched_output

    def _compile_graph_if_enabled(self):
        """Compile LangGraph pipeline if dependency available and enabled."""
        if not self.enable_langgraph:
            return None

        try:
            from langgraph.graph import END, StateGraph
        except Exception:
            return None

        graph = StateGraph(AgentGraphState)
        graph.add_node("pre_process", self._graph_pre_process)
        graph.add_node("core_process", self._graph_core_process)
        graph.add_node("post_process", self._graph_post_process)
        graph.set_entry_point("pre_process")
        graph.add_edge("pre_process", "core_process")
        graph.add_edge("core_process", "post_process")
        graph.add_edge("post_process", END)
        return graph.compile()

    def _run_langgraph(self, input_payload: dict[str, Any], run_id: str) -> dict[str, Any]:
        """Execute through LangGraph with schema validation."""
        try:
            validated_input = validate_schema(input_payload, self.input_schema())
        except SchemaValidationError as e:
            log_event(self.logger, "schema_validation_failed", run_id=run_id, error=str(e))
            raise

        self.execution_state["_run_id"] = run_id
        result = self._compiled_graph.invoke({"input_payload": validated_input})
        final_output = result.get("final_output", {})

        # Validate output
        try:
            validated_output = validate_schema(final_output, self.output_schema())
        except SchemaValidationError as e:
            log_event(self.logger, "schema_validation_failed", run_id=run_id, error=str(e))
            raise

        enriched_output = self._auto_enrich_output(validated_output, run_id)
        return enriched_output

    def _graph_pre_process(self, state: AgentGraphState) -> AgentGraphState:
        run_id = self.execution_state.get("_run_id", "")
        self.execution_trace.append("pre_process")
        prepped = self.pre_process(state.get("input_payload", {}))
        self.execution_state["prepped"] = prepped
        log_event(self.logger, "step_completed", run_id=run_id, step="pre_process")
        return {"prepped": prepped}

    def _graph_core_process(self, state: AgentGraphState) -> AgentGraphState:
        run_id = self.execution_state.get("_run_id", "")
        self.execution_trace.append("core_process")
        core_output = self.core_process(state.get("prepped", {}))
        self.execution_state["core_output"] = core_output
        log_event(self.logger, "step_completed", run_id=run_id, step="core_process")
        return {"core_output": core_output}

    def _graph_post_process(self, state: AgentGraphState) -> AgentGraphState:
        run_id = self.execution_state.get("_run_id", "")
        self.execution_trace.append("post_process")
        final_output = self.post_process(state.get("core_output", {}))
        self.execution_state["final_output"] = final_output
        log_event(self.logger, "step_completed", run_id=run_id, step="post_process")
        return {"final_output": final_output}
