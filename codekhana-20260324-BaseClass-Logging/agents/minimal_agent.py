"""Minimal concrete agent used to validate BaseAgent behavior."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

if __package__ is None or __package__ == "":
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

from common.agent.base_agent import BaseAgent
from common.agent.llm_client import LLMClient


class MinimalAgent(BaseAgent):
    """Deterministic phase-1 agent without infra or LLM dependencies."""

    agent_id = "minimal_agent"
    model_tier = "fast"
    system_prompt = "You are a deterministic test agent."
    task_name = "minimal_agent.run"
    queue_name = "minimal_queue"

    def __init__(self) -> None:
        super().__init__()
        self.llm_client = LLMClient()

    def pre_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        text = str(input_payload.get("text", "")).strip()
        use_llm = bool(input_payload.get("use_llm", False))
        return {"text": text, "use_llm": use_llm}

    def core_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        text = input_payload.get("text", "")
        use_llm = input_payload.get("use_llm", False)
        if not use_llm:
            return {"message": f"processed:{text}", "mode": "deterministic"}

        result = self.llm_client.generate(
            prompt=text,
            model_tier=self.model_tier,
            fallback=lambda p: f"processed:{p}",
        )
        return {"message": result.message, "mode": result.mode, "model": result.model}

    def post_process(self, core_output: dict[str, Any]) -> dict[str, Any]:
        return {"agent": self.agent_id, **core_output}


def main() -> None:
    """Simple local execution entrypoint."""
    agent = MinimalAgent()
    sample = {"text": "hello"}
    result = agent.run(sample)
    print(result)


if __name__ == "__main__":
    main()
