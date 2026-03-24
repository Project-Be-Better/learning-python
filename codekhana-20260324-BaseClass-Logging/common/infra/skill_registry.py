"""Skill/manifest policy registry and validation."""

from __future__ import annotations

from enum import Enum

from common.observability.logger import get_logger, log_event


logger = get_logger(__name__)


class AgentManifestMismatchError(Exception):
    """Raised when an agent manifest drifts from registry policy."""


class SecurityControl(str, Enum):
    """OWASP LLM / Agentic security controls used in policy metadata."""

    LLM01 = "LLM01"
    LLM02 = "LLM02"
    LLM05 = "LLM05"
    LLM09 = "LLM09"
    ASI01 = "ASI01"
    ASI02 = "ASI02"
    ASI03 = "ASI03"
    ASI05 = "ASI05"
    ASI07 = "ASI07"
    ASI08 = "ASI08"

    @property
    def description(self) -> str:
        descriptions = {
            SecurityControl.LLM01: "Prompt injection resistance",
            SecurityControl.LLM02: "Sensitive data protection",
            SecurityControl.LLM05: "Improper output handling prevention",
            SecurityControl.LLM09: "Misinformation risk mitigation",
            SecurityControl.ASI01: "Agent goal hijacking prevention",
            SecurityControl.ASI02: "Tool misuse prevention",
            SecurityControl.ASI03: "Identity and privilege abuse prevention",
            SecurityControl.ASI05: "Repudiation and forensic traceability",
            SecurityControl.ASI07: "Secure inter-agent communication",
            SecurityControl.ASI08: "Cascading failure containment",
        }
        return descriptions[self]


def explain_controls(controls: list[SecurityControl]) -> list[dict[str, str]]:
    """Return code + explanation pairs for reporting and logs."""
    return [{"code": control.value, "description": control.description} for control in controls]


SKILL_REGISTRY: dict[str, dict] = {
    "scoring_agent": {
        "permitted_tools": ["redis_read", "redis_write", "llm_call"],
        "owasp_controls": [
            SecurityControl.LLM01,
            SecurityControl.LLM02,
            SecurityControl.LLM05,
            SecurityControl.ASI01,
            SecurityControl.ASI03,
        ],
        "permitted_tables": {
            "read": ["trips", "telemetry_events"],
            "write": ["trip_scores", "fairness_audit_log", "driver_scores"],
        },
    },
    "minimal_agent": {
        "permitted_tools": ["llm_call"],
        "owasp_controls": [SecurityControl.LLM05],
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

    controls: list[SecurityControl] = policy.get("owasp_controls", [])
    log_event(
        logger,
        "skill_registry_validated",
        agent_id=agent_id,
        owasp_controls=[control.value for control in controls],
        owasp_explanations=explain_controls(controls),
    )
