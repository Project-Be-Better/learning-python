"""Skill/manifest policy registry and validation."""

from __future__ import annotations

from common.observability.logger import get_logger, log_event


logger = get_logger(__name__)


class AgentManifestMismatchError(Exception):
    """Raised when an agent manifest drifts from registry policy."""


SKILL_REGISTRY: dict[str, dict] = {
    "scoring_agent": {
        "permitted_tools": ["redis_read", "redis_write", "llm_call"],
        "owasp_controls": ["LLM01", "LLM02", "LLM05", "ASI01", "ASI03"],
        "permitted_tables": {
            "read": ["trips", "telemetry_events"],
            "write": ["trip_scores", "fairness_audit_log", "driver_scores"],
        },
    },
    "minimal_agent": {
        "permitted_tools": ["llm_call"],
        "owasp_controls": ["LLM05"],
        "permitted_tables": {"read": [], "write": []},
    },
}


def validate_manifest(agent_id: str, manifest_tools: list[str]) -> None:
    """Validate declared tools against registry policy when agent is registered."""
    policy = SKILL_REGISTRY.get(agent_id)
    if policy is None:
        log_event(logger, "agent_not_in_skill_registry", agent_id=agent_id)
        return

    declared = set(manifest_tools)
    registered = set(policy.get("permitted_tools", []))
    if declared != registered:
        extra = sorted(declared - registered)
        missing = sorted(registered - declared)
        raise AgentManifestMismatchError(
            f"Agent '{agent_id}' manifest mismatch. Extra={extra}, Missing={missing}"
        )

    log_event(logger, "skill_registry_validated", agent_id=agent_id, owasp_controls=policy.get("owasp_controls", []))
