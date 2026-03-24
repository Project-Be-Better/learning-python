"""Workflow policy registry used by orchestrator-side planning."""

from __future__ import annotations


class WorkflowRegistry:
    """In-memory workflow definitions with key-template resolution."""

    _workflows: dict[str, dict] = {
        "trip_analysis": {
            "workflow_id": "trip_analysis",
            "steps": [
                {
                    "step_index": 1,
                    "agent": "scoring_agent",
                    "queue": "scoring_queue",
                    "priority": 9,
                    "permitted_tools": ["redis_read", "redis_write", "llm_call"],
                    "allowed_inputs": [
                        "trip:{trip_id}:context",
                        "trip:{trip_id}:smoothness_logs",
                        "trip:{trip_id}:harsh_events",
                    ],
                    "expected_outputs": ["trip:{trip_id}:scoring_output"],
                }
            ],
        }
    }

    def get_workflow(self, workflow_id: str) -> dict:
        if workflow_id not in self._workflows:
            raise KeyError(f"workflow '{workflow_id}' not found")
        return self._workflows[workflow_id]

    def get_step(self, workflow_id: str, step_index: int) -> dict:
        workflow = self.get_workflow(workflow_id)
        for step in workflow.get("steps", []):
            if step.get("step_index") == step_index:
                return step
        raise KeyError(f"step {step_index} not found in workflow '{workflow_id}'")

    def resolve_keys(self, step: dict, trip_id: str) -> dict:
        resolved = dict(step)
        resolved["allowed_inputs"] = [k.replace("{trip_id}", trip_id) for k in step.get("allowed_inputs", [])]
        resolved["expected_outputs"] = [k.replace("{trip_id}", trip_id) for k in step.get("expected_outputs", [])]
        return resolved


workflow_registry = WorkflowRegistry()
