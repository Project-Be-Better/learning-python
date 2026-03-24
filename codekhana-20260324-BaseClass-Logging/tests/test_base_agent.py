"""Phase-1 tests for BaseAgent and MinimalAgent lifecycle."""

from __future__ import annotations

import json
import pytest

from agents.minimal_agent import MinimalAgent
from common.agent.base_agent import BaseAgent, SchemaValidationError, validate_schema
from common.infra.intent_gate import IntentGateError
from common.infra.skill_registry import AgentManifestMismatchError
from common.observability.logger import _clear_logger_cache



def test_manifest_is_initialized() -> None:
    agent = MinimalAgent()
    assert agent.manifest.agent_id == "minimal_agent"
    assert agent.manifest.model_tier == "fast"



def test_run_executes_hooks_in_order() -> None:
    agent = MinimalAgent()

    output = agent.run({"text": "abc"})

    assert output["message"] == "processed:abc"
    assert output["agent"] == "minimal_agent"
    assert output["mode"] == "deterministic"
    assert agent.execution_trace == ["pre_process", "core_process", "post_process"]



def test_run_rejects_non_dict_payload() -> None:
    agent = MinimalAgent()

    with pytest.raises(ValueError, match="input_payload must be a dictionary"):
        agent.run("invalid")  # type: ignore[arg-type]


def test_run_resets_execution_state_each_call() -> None:
    agent = MinimalAgent()

    first = agent.run({"text": "first"})
    second = agent.run({"text": "second"})

    assert first["message"] == "processed:first"
    assert second["message"] == "processed:second"
    assert second["agent"] == "minimal_agent"
    assert second["mode"] == "deterministic"
    assert agent.execution_trace == ["pre_process", "core_process", "post_process"]
    assert agent.execution_state["final_output"]["message"] == "processed:second"


def test_pre_process_normalizes_whitespace() -> None:
    agent = MinimalAgent()

    output = agent.run({"text": "  hello  "})

    assert output["message"] == "processed:hello"


def test_llm_mode_falls_back_without_api_key(monkeypatch) -> None:
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    agent = MinimalAgent()

    output = agent.run({"text": "hello", "use_llm": True})

    assert output["message"] == "processed:hello"
    assert output["mode"] == "fallback"


def test_run_emits_structured_lifecycle_logs(
    monkeypatch,
    capfd: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.delenv("LOG_FORMAT", raising=False)
    _clear_logger_cache()

    agent = MinimalAgent()

    agent.run({"text": "abc"})
    captured = capfd.readouterr()
    records = [json.loads(line) for line in captured.out.splitlines() if line.strip()]
    events = {record.get("event") for record in records}

    assert "run_started" in events
    assert "step_completed" in events
    assert "run_completed" in events


def test_base_agent_retries_when_configured() -> None:
    class FlakyAgent(BaseAgent):
        agent_id = "flaky_agent"
        task_name = "flaky_agent.run"
        max_retries = 1
        retry_backoff_seconds = 0.0
        retry_exceptions = (RuntimeError,)

        def __init__(self) -> None:
            super().__init__()
            self.calls = 0

        def core_process(self, input_payload: dict[str, object]) -> dict[str, object]:
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("transient")
            return {"ok": True}

    agent = FlakyAgent()
    output = agent.run({})

    assert output["ok"] is True
    assert agent.calls == 2
    assert agent.execution_state["attempt"] == 2


def test_base_agent_does_not_retry_unlisted_exceptions() -> None:
    class StrictRetryAgent(BaseAgent):
        agent_id = "strict_retry_agent"
        task_name = "strict_retry_agent.run"
        max_retries = 3
        retry_backoff_seconds = 0.0
        retry_exceptions = (ValueError,)

        def __init__(self) -> None:
            super().__init__()
            self.calls = 0

        def core_process(self, input_payload: dict[str, object]) -> dict[str, object]:
            self.calls += 1
            raise RuntimeError("non_retryable")

    agent = StrictRetryAgent()

    with pytest.raises(RuntimeError, match="non_retryable"):
        agent.run({})

    assert agent.calls == 1


def test_base_agent_output_schema_preserves_extra_fields() -> None:
    class OutputSchemaAgent(BaseAgent):
        agent_id = "output_schema_agent"
        task_name = "output_schema_agent.run"

        def output_schema(self) -> dict[str, object]:
            return {"required_field": {"type": "str", "required": True}}

        def core_process(self, input_payload: dict[str, object]) -> dict[str, object]:
            return {
                "required_field": "ok",
                "extra_field": 42,
            }

    agent = OutputSchemaAgent()
    output = agent.run({})

    assert output["required_field"] == "ok"
    assert output["extra_field"] == 42


def test_validate_schema_supports_nested_dict_and_list() -> None:
    schema = {
        "context": {
            "type": "dict",
            "required": True,
            "schema": {
                "trip_id": {"type": "str", "required": True},
                "trip_summary": {
                    "type": "dict",
                    "required": True,
                    "schema": {
                        "distance_km": {"type": "float", "required": True, "min": 0.1},
                    },
                },
            },
        },
        "harsh_events": {
            "type": "list",
            "required": True,
            "items": {
                "type": "dict",
                "schema": {
                    "event_type": {"type": "str", "required": True, "enum": ["harsh_brake", "harsh_turn"]},
                },
            },
        },
    }

    payload = {
        "context": {
            "trip_id": "trip-1",
            "trip_summary": {"distance_km": "12.5"},
        },
        "harsh_events": [{"event_type": "harsh_brake"}],
    }

    validated = validate_schema(payload, schema)
    assert validated["context"]["trip_summary"]["distance_km"] == 12.5


def test_validate_schema_bool_parsing_is_strict() -> None:
    schema = {
        "enabled": {"type": "bool", "required": True},
    }

    validated = validate_schema({"enabled": "true"}, schema)
    assert validated["enabled"] is True

    with pytest.raises(SchemaValidationError):
        validate_schema({"enabled": "maybe"}, schema)


def test_base_agent_lifecycle_hooks_can_be_overridden() -> None:
    class HookAgent(BaseAgent):
        agent_id = "hook_agent"
        task_name = "hook_agent.run"

        def __init__(self) -> None:
            super().__init__()
            self.failure_called = False

        def core_process(self, input_payload: dict[str, object]) -> dict[str, object]:
            if input_payload.get("fail"):
                raise RuntimeError("hook-fail")
            return {"ok": True}

        def on_run_success(self, final_output: dict[str, object]) -> dict[str, object]:
            final_output["hooked"] = True
            return final_output

        def on_run_failure(self, exc: Exception) -> None:
            self.failure_called = True

    agent = HookAgent()

    ok = agent.run({})
    assert ok["hooked"] is True

    with pytest.raises(RuntimeError, match="hook-fail"):
        agent.run({"fail": True})
    assert agent.failure_called is True


def test_base_agent_accepts_secure_envelope_when_gate_enabled() -> None:
    from common.infra.intent_gate import IntentCapsule

    class SecureEchoAgent(BaseAgent):
        agent_id = "secure_echo_agent"
        task_name = "secure_echo_agent.run"
        enforce_intent_gate = True
        expected_step = 1
        permitted_tools = ["redis_read"]

        def core_process(self, input_payload: dict[str, object]) -> dict[str, object]:
            return {"ok": True, "text": input_payload.get("text", "")}

    capsule = IntentCapsule(
        trip_id="trip-sec-1",
        agent="secure_echo_agent",
        priority=9,
        step_index=1,
        issued_by="orchestrator",
        allowed_inputs=["trip:trip-sec-1:context"],
        expected_outputs=["trip:trip-sec-1:echo_output"],
        permitted_tools=["redis_read"],
    )
    capsule.hmac_seal = capsule.compute_hmac()

    agent = SecureEchoAgent()
    output = agent.run(
        {
            "intent_capsule": {
                "trip_id": capsule.trip_id,
                "agent": capsule.agent,
                "priority": capsule.priority,
                "step_index": capsule.step_index,
                "issued_by": capsule.issued_by,
                "allowed_inputs": capsule.allowed_inputs,
                "expected_outputs": capsule.expected_outputs,
                "permitted_tools": capsule.permitted_tools,
                "ttl": capsule.ttl,
                "issued_at": capsule.issued_at,
                "hmac_seal": capsule.hmac_seal,
            },
            "input_payload": {"text": "hello"},
        }
    )

    assert output["ok"] is True
    assert output["text"] == "hello"


def test_base_agent_rejects_missing_capsule_when_gate_enabled() -> None:
    class SecureOnlyAgent(BaseAgent):
        agent_id = "secure_only_agent"
        task_name = "secure_only_agent.run"
        enforce_intent_gate = True

        def core_process(self, input_payload: dict[str, object]) -> dict[str, object]:
            return {"ok": True}

    agent = SecureOnlyAgent()
    with pytest.raises(IntentGateError, match="intent_capsule_required"):
        agent.run({"text": "legacy"})


def test_strict_manifest_validation_raises_on_drift() -> None:
    class DriftAgent(BaseAgent):
        agent_id = "scoring_agent"  # registered in skill registry
        task_name = "drift_agent.run"
        strict_manifest_validation = True
        permitted_tools = ["redis_read"]  # intentionally incomplete

        def core_process(self, input_payload: dict[str, object]) -> dict[str, object]:
            return {"ok": True}

    with pytest.raises(AgentManifestMismatchError):
        DriftAgent()
