"""Minimal BaseAgent lifecycle for Phase 1 scaffold."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AgentManifest:
    """Static identity and routing metadata for an agent."""

    agent_id: str
    model_tier: str = "fast"
    system_prompt: str = ""
    task_name: str = ""
    queue_name: str = ""


class BaseAgent:
    """Smallest runnable agent base class with lifecycle hooks."""

    agent_id: str = "base_agent"
    model_tier: str = "fast"
    system_prompt: str = ""
    task_name: str = ""
    queue_name: str = ""

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

    def run(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Run pre-process, core-process, and post-process in order."""
        if not isinstance(input_payload, dict):
            raise ValueError("input_payload must be a dictionary")

        self.execution_trace.append("pre_process")
        prepped = self.pre_process(input_payload)
        self.execution_state["prepped"] = prepped

        self.execution_trace.append("core_process")
        core_output = self.core_process(prepped)
        self.execution_state["core_output"] = core_output

        self.execution_trace.append("post_process")
        final_output = self.post_process(core_output)
        self.execution_state["final_output"] = final_output

        return final_output

    def pre_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Hook for subclass input transformation."""
        return input_payload

    def core_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Core process. Subclasses should override this."""
        return input_payload

    def post_process(self, core_output: dict[str, Any]) -> dict[str, Any]:
        """Hook for subclass output transformation."""
        return core_output
