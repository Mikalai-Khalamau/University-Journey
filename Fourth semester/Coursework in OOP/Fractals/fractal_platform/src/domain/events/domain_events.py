from dataclasses import dataclass
from uuid import UUID

from src.domain.value_objects.task_status import TaskStatus


@dataclass(frozen=True)
class TaskStatusChangedEvent:
    task_id: UUID
    status: TaskStatus
    message: str | None = None
