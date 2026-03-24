"""Tests for environment-based logger format behavior."""

from __future__ import annotations

import json

from common.observability.logger import _clear_logger_cache, get_logger, log_event


def test_default_format_is_text_in_non_production(
    monkeypatch,
    capfd,
) -> None:
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("LOG_FORMAT", raising=False)
    _clear_logger_cache()

    logger = get_logger("agent.test")
    log_event(logger, "run_started", run_id="r1", agent_id="a1")

    captured = capfd.readouterr().out.strip()
    assert captured
    assert captured.startswith("{") is False
    assert "run_started" in captured
    assert "INFO" in captured


def test_production_defaults_to_json(
    monkeypatch,
    capfd,
) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.delenv("LOG_FORMAT", raising=False)
    _clear_logger_cache()

    logger = get_logger("agent.test")
    log_event(logger, "run_started", run_id="r2", agent_id="a2")

    captured = capfd.readouterr().out.strip()
    payload = json.loads(captured)
    assert payload["event"] == "run_started"
    assert payload["run_id"] == "r2"
    assert payload["agent_id"] == "a2"


def test_log_format_override_to_text_even_in_production(
    monkeypatch,
    capfd,
) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("LOG_FORMAT", "text")
    _clear_logger_cache()

    logger = get_logger("agent.test")
    log_event(logger, "run_started", run_id="r3", agent_id="a3")

    captured = capfd.readouterr().out.strip()
    assert captured.startswith("{") is False
    assert "run_started" in captured
