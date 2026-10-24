from __future__ import annotations

from src.core.patterns.observer import Observer
from src.domain.value_objects.task_status import TaskStatus


class UINotifier(Observer):
    """
    Observer для отправки уведомлений в интерфейс.
    """

    def __init__(self) -> None:
        self._pending_notifications: dict[str, list[dict]] = {}

    def update(self, event_name: str, payload: dict) -> None:
        if event_name != "task_status":
            return

        task_id = payload.get("task_id")
        status = payload.get("status")
        message = payload.get("message")
        user_id = payload.get("user_id")

        if not user_id or status not in (TaskStatus.COMPLETED, TaskStatus.FAILED):
            return

        notification = {
            "task_id": str(task_id),
            "status": status,
            "message": message,
            "timestamp": payload.get("timestamp"),
            "read": False,
        }

        if user_id not in self._pending_notifications:
            self._pending_notifications[user_id] = []
        self._pending_notifications[user_id].append(notification)


    def get_pending(self, user_id: str) -> list[dict]:
        """Возвращает и помечает как прочитанные уведомления пользователя."""
        notifications = self._pending_notifications.get(user_id, [])
        for n in notifications:
            n["read"] = True
        self._pending_notifications[user_id] = [n for n in notifications if not n["read"]]
        return notifications

    def clear_user(self, user_id: str) -> None:
        """Очистить все уведомления пользователя."""
        self._pending_notifications.pop(user_id, None)