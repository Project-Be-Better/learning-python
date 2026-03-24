"""Intent capsule and gate verification utilities."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from common.infra.scoped_token import ScopedToken


SHARED_SECRET = os.environ.get("TRACEDATA_HMAC_SECRET", "dev-secret-change-in-prod")


@dataclass
class IntentCapsule:
    """Signed runtime authorization envelope for one agent execution."""

    trip_id: str
    agent: str
    priority: int
    step_index: int
    issued_by: str
    allowed_inputs: list[str] = field(default_factory=list)
    expected_outputs: list[str] = field(default_factory=list)
    permitted_tools: list[str] = field(default_factory=list)
    ttl: int = 3600
    issued_at: str = ""
    hmac_seal: str = ""
    token: ScopedToken | None = None

    def __post_init__(self) -> None:
        if not self.issued_at:
            self.issued_at = datetime.now(timezone.utc).isoformat()

    def _canonical_payload(self) -> str:
        payload = {
            "trip_id": self.trip_id,
            "agent": self.agent,
            "priority": self.priority,
            "step_index": self.step_index,
            "issued_by": self.issued_by,
            "allowed_inputs": self.allowed_inputs,
            "expected_outputs": self.expected_outputs,
            "permitted_tools": self.permitted_tools,
            "ttl": self.ttl,
            "issued_at": self.issued_at,
            "token_id": self.token.token_id if self.token else None,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def compute_hmac(self) -> str:
        data = self._canonical_payload().encode("utf-8")
        return hmac.new(SHARED_SECRET.encode("utf-8"), data, hashlib.sha256).hexdigest()

    def is_hmac_valid(self) -> bool:
        if not self.hmac_seal:
            return False
        expected = self.compute_hmac()
        return hmac.compare_digest(self.hmac_seal, expected)

    def is_expired(self) -> bool:
        issued = datetime.fromisoformat(self.issued_at)
        if issued.tzinfo is None:
            issued = issued.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) >= (issued + timedelta(seconds=self.ttl))


class IntentGateError(Exception):
    """Raised when intent verification fails."""


class IntentGate:
    """Verifies capsule schema, signature, freshness, and step sequencing."""

    def verify(self, capsule: IntentCapsule, expected_step: int) -> None:
        if not capsule.trip_id or not capsule.agent:
            raise IntentGateError("schema_invalid: trip_id/agent required")

        if not capsule.is_hmac_valid():
            raise IntentGateError("hmac_mismatch: invalid capsule signature")

        if capsule.is_expired() or (capsule.token and capsule.token.is_expired()):
            raise IntentGateError("token_expired: capsule/token expired")

        if capsule.step_index != expected_step:
            raise IntentGateError(
                f"sequence_violation: expected step {expected_step}, got {capsule.step_index}"
            )


intent_gate = IntentGate()
