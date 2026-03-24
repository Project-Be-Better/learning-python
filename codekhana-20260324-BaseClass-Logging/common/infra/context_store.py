"""Context store abstraction (Redis stub for local development)."""

from __future__ import annotations

import json
from typing import Any

from common.observability.logger import get_logger, log_event


logger = get_logger(__name__)
_memory_store: dict[str, str] = {}
_events_stream: dict[str, list[dict[str, Any]]] = {}


class ContextStore:
    """Abstracts runtime context reads/writes away from raw Redis clients."""

    def get(self, key: str) -> dict[str, Any] | None:
        raw = _memory_store.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            log_event(logger, "context_get_decode_failed", key=key)
            return None

    def set(self, key: str, value: dict[str, Any], ttl: int = 7200) -> None:
        _memory_store[key] = json.dumps(value)
        log_event(logger, "context_set", key=key, ttl=ttl)

    def publish(self, channel: str, event: dict[str, Any]) -> None:
        bucket = _events_stream.setdefault(channel, [])
        bucket.append(event)
        log_event(logger, "context_publish", channel=channel, event_type=event.get("status", "unknown"))

    def read_channel(self, channel: str) -> list[dict[str, Any]]:
        """Testing helper: inspect published events for a channel."""
        return list(_events_stream.get(channel, []))

    def delete(self, key: str) -> None:
        _memory_store.pop(key, None)


context_store = ContextStore()
