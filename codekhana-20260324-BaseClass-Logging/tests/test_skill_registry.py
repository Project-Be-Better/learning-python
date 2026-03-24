"""Tests for skill registry security control metadata."""

from __future__ import annotations

from common.infra.skill_registry import SecurityControl, SKILL_REGISTRY, explain_controls


def test_security_control_enum_has_description() -> None:
    assert SecurityControl.LLM05.description == "Improper output handling prevention"
    assert SecurityControl.ASI03.description == "Identity and privilege abuse prevention"


def test_skill_registry_controls_are_typed_enums() -> None:
    controls = SKILL_REGISTRY["scoring_agent"]["owasp_controls"]
    assert all(isinstance(control, SecurityControl) for control in controls)


def test_explain_controls_returns_code_and_description() -> None:
    explained = explain_controls([SecurityControl.LLM01, SecurityControl.ASI01])
    assert explained == [
        {"code": "LLM01", "description": "Prompt injection resistance"},
        {"code": "ASI01", "description": "Agent goal hijacking prevention"},
    ]
