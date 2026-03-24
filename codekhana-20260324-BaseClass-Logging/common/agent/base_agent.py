"""Thick BaseAgent with schema validation and auto-enrichment."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import perf_counter
from typing import Any, TypedDict
from uuid import uuid4

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


def validate_schema(data: dict[str, Any], schema: dict[str, Any] | None) -> dict[str, Any]:
    """
    Lightweight schema validation with type coercion and bounds checking.

    Schema format:
    {"field_name": {"type": "str", "required": True, "default": None, "min": 0, "max": 100}}

    Returns validated and coerced data, raises SchemaValidationError on failure.
    """
    if schema is None:
        return data

    validated = {}
    for field_name, field_spec in schema.items():
        field_type = field_spec.get("type", "str")
        required = field_spec.get("required", False)
        default = field_spec.get("default")
        min_val = field_spec.get("min")
        max_val = field_spec.get("max")

        if field_name not in data:
            if required and default is None:
                raise SchemaValidationError(f"Required field missing: {field_name}")
            validated[field_name] = default
            continue

        value = data[field_name]

        # Type coercion / type validation
        try:
            if field_type == "int":
                value = int(value)
            elif field_type == "float":
                value = float(value)
            elif field_type == "str":
                value = str(value)
            elif field_type == "bool":
                value = bool(value)
            elif field_type == "dict":
                if not isinstance(value, dict):
                    raise TypeError(f"expected dict, got {type(value).__name__}")
            elif field_type == "list":
                if not isinstance(value, list):
                    raise TypeError(f"expected list, got {type(value).__name__}")
            else:
                # Unknown types are treated as pass-through to avoid destructive coercion.
                value = value
        except (ValueError, TypeError) as e:
            raise SchemaValidationError(
                f"Field {field_name}: cannot coerce to {field_type}: {e}"
            )

        # Bounds checking
        if min_val is not None and value < min_val:
            raise SchemaValidationError(
                f"Field {field_name}: value {value} below minimum {min_val}"
            )
        if max_val is not None and value > max_val:
            raise SchemaValidationError(
                f"Field {field_name}: value {value} above maximum {max_val}"
            )

        validated[field_name] = value

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
    enable_langgraph: bool = True
    auto_enrich_output: bool = True
    max_retries: int = 0

    def __init__(self) -> None:
        self.manifest = AgentManifest(
            agent_id=self.agent_id,
            model_tier=self.model_tier,
            system_prompt=self.system_prompt,
            task_name=self.task_name,
            queue_name=self.queue_name,
        )
        self.execution_trace: list[str] = []
        self.execution_state: dict[str, Any] = {}
        self.logger = get_logger(f"agent.{self.agent_id}")
        self._compiled_graph = self._compile_graph_if_enabled()

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

    def run(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Execute agent lifecycle: pre_process → core_process → post_process."""
        if not isinstance(input_payload, dict):
            raise ValueError("input_payload must be a dictionary")

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
            input_keys=sorted(input_payload.keys()),
        )

        try:
            if self._compiled_graph is not None:
                self.execution_state["engine"] = "langgraph"
                final_output = self._run_langgraph(input_payload, run_id)
            else:
                self.execution_state["engine"] = "sequential"
                final_output = self._run_sequential(input_payload, run_id)

            duration_ms = round((perf_counter() - started_at) * 1000, 3)
            log_event(
                self.logger,
                "run_completed",
                run_id=run_id,
                agent_id=self.agent_id,
                status="ok",
                duration_ms=duration_ms,
            )
            return final_output
        except Exception as exc:
            duration_ms = round((perf_counter() - started_at) * 1000, 3)
            log_event(
                self.logger,
                "run_failed",
                run_id=run_id,
                agent_id=self.agent_id,
                status="error",
                duration_ms=duration_ms,
                error_type=type(exc).__name__,
                error_message=str(exc),
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
