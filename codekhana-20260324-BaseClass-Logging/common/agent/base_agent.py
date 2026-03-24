"""Minimal BaseAgent lifecycle for Phase 1 scaffold."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import perf_counter
from typing import Any
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


class BaseAgent(ABC):
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
        self.logger = get_logger(f"agent.{self.agent_id}")

    def run(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """
        Run pre-process, core-process, and post-process in order
        """
        if not isinstance(input_payload, dict):
            raise ValueError("input_payload must be a dictionary")

        run_id = str(uuid4())
        started_at = perf_counter()

        # Keep state scoped to a single execution.
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
            self.execution_trace.append("pre_process")
            prepped = self.pre_process(input_payload)
            self.execution_state["prepped"] = prepped
            log_event(self.logger, "step_completed", run_id=run_id, step="pre_process")

            self.execution_trace.append("core_process")
            core_output = self.core_process(prepped)
            self.execution_state["core_output"] = core_output
            log_event(self.logger, "step_completed", run_id=run_id, step="core_process")

            self.execution_trace.append("post_process")
            final_output = self.post_process(core_output)
            self.execution_state["final_output"] = final_output
            log_event(self.logger, "step_completed", run_id=run_id, step="post_process")

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

    def pre_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Hook for subclass input transformation."""
        return input_payload

    @abstractmethod
    def core_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Core process. Concrete agents must implement this."""

    def post_process(self, core_output: dict[str, Any]) -> dict[str, Any]:
        """Hook for subclass output transformation."""
        return core_output
