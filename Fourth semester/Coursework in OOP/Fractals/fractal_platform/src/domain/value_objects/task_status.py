from __future__ import annotations

from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

    def can_transition_to(self, target: "TaskStatus") -> bool:
        transitions = {
            TaskStatus.PENDING: {TaskStatus.PROCESSING, TaskStatus.FAILED},
            TaskStatus.PROCESSING: {TaskStatus.COMPLETED, TaskStatus.FAILED},
            TaskStatus.COMPLETED: set(),
            TaskStatus.FAILED: set(),
        }
        return target in transitions[self]
