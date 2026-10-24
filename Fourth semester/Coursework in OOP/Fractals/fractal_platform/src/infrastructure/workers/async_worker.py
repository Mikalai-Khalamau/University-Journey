from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any
from uuid import UUID

from src.core.patterns.observer import Subject
from src.domain.value_objects.task_status import TaskStatus


class AsyncFractalWorker(Subject):
    def __init__(self, run_generation) -> None:
        super().__init__()
        self._run_generation = run_generation
        self._executor = ThreadPoolExecutor()

    def submit(self, task_id: UUID, job: dict[str, Any]) -> None:
        self.notify("task_status", {"task_id": task_id, "status": TaskStatus.PENDING})
        self._executor.submit(self._execute, task_id, job)

    def _execute(self, task_id: UUID, job: dict[str, Any]) -> None:
        self.notify("task_status", {
            "task_id": task_id,
            "status": TaskStatus.PENDING,
            "user_id": str(job["user_id"]),
        })

        try:
            fractal_id = self._run_generation(
                job["params"],
                job["user_id"],
                job["name"],
                job.get("tags", ["basic"]),
            )
            self.notify("task_status", {
                "task_id": task_id,
                "status": TaskStatus.COMPLETED,
                "fractal_id": str(fractal_id),
                "user_id": str(job["user_id"]),
            })
        except Exception as exc:
            self.notify("task_status", {
                "task_id": task_id,
                "status": TaskStatus.FAILED,
                "message": str(exc),
                "user_id": str(job["user_id"]),
            })