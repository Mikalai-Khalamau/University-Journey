from __future__ import annotations

from uuid import UUID

from src.core.patterns.observer import Observer
from src.domain.value_objects.task_status import TaskStatus


class TaskStatusTracker(Observer):
    def __init__(self) -> None:
        self._statuses: dict[UUID, dict] = {}

    def create(self, task_id: UUID, user_id: UUID) -> None:
        self._statuses[task_id] = {
            "status": TaskStatus.PENDING,
            "message": None,
            "fractal_id": None,
            "user_id": str(user_id),
        }

    def get(self, task_id: UUID, user_id: UUID) -> dict | None:
        data = self._statuses.get(task_id)
        if data is None:
            return None
        if data.get("user_id") != str(user_id):
            return None
        return data

    def update(self, event_name: str, payload: dict) -> None:
        task_id = payload["task_id"]
        if task_id not in self._statuses:
            return
        self._statuses[task_id] = {
            "status": payload.get("status", TaskStatus.PENDING),
            "message": payload.get("message"),
            "fractal_id": payload.get("fractal_id"),
            "user_id": self._statuses[task_id].get("user_id"),
        }
