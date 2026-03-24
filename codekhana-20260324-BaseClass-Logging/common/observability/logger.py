"""Structured logger utilities for agent runtime events.

Format behavior:
- Production defaults to JSON for machine ingestion (ELK/PLG).
- Non-production defaults to one-line text for readability.
- `LOG_FORMAT` can override with `json` or `text` in any environment.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import UTC, datetime
from typing import Any


class JsonFormatter(logging.Formatter):
    """Format log records as JSON lines."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        extra_payload = getattr(record, "payload", None)
        if isinstance(extra_payload, dict):
            payload.update(extra_payload)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


class TextFormatter(logging.Formatter):
    """Format log records as one-line text while keeping key fields visible."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now(UTC).isoformat()
        payload = getattr(record, "payload", {})
        if not isinstance(payload, dict):
            payload = {}

        run_id = payload.get("run_id", "-")
        event = payload.get("event", record.getMessage())

        reserved = {"event", "run_id"}
        extras = [f"{k}={payload[k]}" for k in sorted(payload) if k not in reserved]
        extras_blob = f" {' '.join(extras)}" if extras else ""

        return f"{timestamp} {run_id} {record.levelname} {record.name}: {event}{extras_blob}"


_LOGGER_CACHE: dict[str, logging.Logger] = {}


def _resolve_log_format() -> str:
    """Resolve active log format from environment.

    Precedence:
    1. LOG_FORMAT (`json` or `text`)
    2. ENVIRONMENT (`production` -> `json`)
    3. default (`text`)
    """
    explicit = os.getenv("LOG_FORMAT", "").strip().lower()
    if explicit in {"json", "text"}:
        return explicit

    environment = os.getenv("ENVIRONMENT", "").strip().lower()
    if environment in {"prod", "production"}:
        return "json"

    return "text"


def _build_formatter(log_format: str) -> logging.Formatter:
    if log_format == "json":
        return JsonFormatter()
    return TextFormatter()


def _clear_logger_cache() -> None:
    """Test helper to clear cached logger instances."""
    _LOGGER_CACHE.clear()


def get_logger(name: str) -> logging.Logger:
    """Return a stdout logger configured using environment-based format."""
    log_format = _resolve_log_format()
    cache_key = f"{name}:{log_format}"
    if cache_key in _LOGGER_CACHE:
        cached = _LOGGER_CACHE[cache_key]
        for handler in cached.handlers:
            if isinstance(handler, logging.StreamHandler) and handler.stream is not sys.stdout:
                handler.setStream(sys.stdout)
        return cached

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Ensure format changes are respected if env changed across runs/tests.
    logger.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_build_formatter(log_format))
    logger.addHandler(handler)

    _LOGGER_CACHE[cache_key] = logger
    return logger


def get_json_logger(name: str) -> logging.Logger:
    """Backward-compatible helper.

    Note: this now returns the environment-selected format. Prefer `get_logger`.
    """
    return get_logger(name)


def log_event(logger: logging.Logger, event: str, **fields: Any) -> None:
    """Emit one structured event record."""
    logger.info(event, extra={"payload": {"event": event, **fields}})
