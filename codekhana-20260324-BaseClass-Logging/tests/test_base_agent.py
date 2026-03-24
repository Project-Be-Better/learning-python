"""Phase-1 tests for BaseAgent and MinimalAgent lifecycle."""

from __future__ import annotations

import pytest

from agents.minimal_agent import MinimalAgent



def test_manifest_is_initialized() -> None:
    agent = MinimalAgent()
    assert agent.manifest.agent_id == "minimal_agent"
    assert agent.manifest.model_tier == "fast"



def test_run_executes_hooks_in_order() -> None:
    agent = MinimalAgent()

    output = agent.run({"text": "abc"})

    assert output["message"] == "processed:abc"
    assert output["_pre_processed"] is True
    assert output["_core_processed"] is True
    assert output["_post_processed"] is True
    assert agent.execution_trace == ["pre_process", "core_process", "post_process"]



def test_run_rejects_non_dict_payload() -> None:
    agent = MinimalAgent()

    with pytest.raises(ValueError, match="input_payload must be a dictionary"):
        agent.run("invalid")  # type: ignore[arg-type]
