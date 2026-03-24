"""Scoped token model for trip/agent-bound access control."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ScopedToken:
    """Short-lived token with explicit read/write key scopes."""

    token_id: str
    agent: str
    expires_at: str
    read_keys: list[str] = field(default_factory=list)
    write_keys: list[str] = field(default_factory=list)

    def is_expired(self) -> bool:
        """Return True if token expiry time is in the past."""
        expires = datetime.fromisoformat(self.expires_at)
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) >= expires

    def can_read(self, key: str) -> bool:
        return key in self.read_keys

    def can_write(self, key: str) -> bool:
        return key in self.write_keys
