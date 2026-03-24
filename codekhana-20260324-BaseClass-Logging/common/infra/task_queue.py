"""Task queue abstraction (Celery-compatible stub for local runtime)."""

from __future__ import annotations

import os
from typing import Callable

from common.observability.logger import get_logger, log_event


logger = get_logger(__name__)
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")


class TaskQueue:
    """Queue registration and dispatch facade."""

    def __init__(self) -> None:
        self._registered: dict[str, Callable] = {}

    def register(self, task_name: str, queue_name: str, handler: Callable) -> None:
        self._registered[task_name] = handler
        log_event(
            logger,
            "celery_worker_registered",
            task_name=task_name,
            queue=queue_name,
            broker=CELERY_BROKER_URL,
        )

    def dispatch(self, task_name: str, payload: dict, priority: int = 9) -> str:
        task_id = f"stub-{task_name}-{abs(hash(str(payload))) % 1000000}"
        log_event(logger, "celery_task_dispatched", task_name=task_name, priority=priority, task_id=task_id)
        return task_id


task_queue = TaskQueue()
