"""Database writer abstraction with permission checks (stub backend)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from common.observability.logger import get_logger, log_event


logger = get_logger(__name__)


class UnauthorisedTableAccessError(Exception):
    """Raised when attempted table access is not permitted for an agent."""


class DBWriter:
    """Write/read abstraction layer for agent persistence operations."""

    def __init__(self) -> None:
        self._permitted_tables: dict[str, list[str]] = {"read": [], "write": []}

    def configure(self, permitted_tables: dict[str, list[str]]) -> None:
        self._permitted_tables = {
            "read": list(permitted_tables.get("read", [])),
            "write": list(permitted_tables.get("write", [])),
        }

    def insert(self, table: str, record: dict[str, Any]) -> None:
        self._check_write_permission(table)
        payload = dict(record)
        payload["created_at"] = datetime.now(timezone.utc).isoformat()
        log_event(logger, "db_insert", table=table, record_keys=sorted(payload.keys()))

    def update(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> None:
        self._check_write_permission(table)
        payload = dict(values)
        payload["updated_at"] = datetime.now(timezone.utc).isoformat()
        log_event(logger, "db_update", table=table, where=where, value_keys=sorted(payload.keys()))

    def select(self, table: str, where: dict[str, Any]) -> list[dict[str, Any]]:
        if table not in self._permitted_tables.get("read", []):
            raise UnauthorisedTableAccessError(f"read denied for table {table}")
        log_event(logger, "db_select", table=table, where=where)
        return []

    def write_audit(self, event: dict[str, Any]) -> None:
        payload = dict(event)
        payload["created_at"] = datetime.now(timezone.utc).isoformat()
        log_event(logger, "audit_log_write", event_keys=sorted(payload.keys()))

    def write_forensic_snapshot(self, snapshot: dict[str, Any]) -> None:
        payload = dict(snapshot)
        payload["created_at"] = datetime.now(timezone.utc).isoformat()
        log_event(logger, "forensic_snapshot_write", snapshot=payload)

    def _check_write_permission(self, table: str) -> None:
        if table not in self._permitted_tables.get("write", []):
            raise UnauthorisedTableAccessError(f"write denied for table {table}")


db_writer = DBWriter()
