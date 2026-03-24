"""Phase-1 tests for BaseAgent and MinimalAgent lifecycle."""

from __future__ import annotations

import json
import pytest

from agents.minimal_agent import MinimalAgent
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
