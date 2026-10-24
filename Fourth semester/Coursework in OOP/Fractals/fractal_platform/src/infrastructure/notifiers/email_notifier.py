from __future__ import annotations

import smtplib
from email.message import EmailMessage
from src.core.patterns.observer import Observer
from src.domain.value_objects.task_status import TaskStatus


class EmailNotifier(Observer):
    """
    Observer для отправки email-уведомлений.
    """

    def __init__(
            self,
            smtp_host: str = "localhost",
            smtp_port: int = 25,
            from_email: str = "noreply@fractal.platform",
            use_tls: bool = False,
    ) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.from_email = from_email
        self.use_tls = use_tls

    def update(self, event_name: str, payload: dict) -> None:
        if event_name != "task_status":
            return

        status = payload.get("status")
        if status not in (TaskStatus.COMPLETED, TaskStatus.FAILED):
            return

        task_id = payload.get("task_id")
        user_id = payload.get("user_id")
        message = payload.get("message")

        # self._send_email(email, status, task_id, message)

    def _send_email(self, to_email: str, status: str, task_id: str, message: str | None) -> None:
        """Реальная отправка email."""
        subject = f"Fractal Platform: {'Готово!' if status == TaskStatus.COMPLETED else 'Ошибка генерации'}"
        body = (
            f"Задача {task_id}\n\n"
            f"Статус: {status}\n"
            f"{'Ваш фрактал готов к просмотру!' if status == TaskStatus.COMPLETED else f'Детали: {message}'}\n\n"
            f"С уважением,\nFractal Platform"
        )

        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = to_email

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.send_message(msg)
            print(f"[EmailNotifier] Email отправлен на {to_email}")
        except Exception as e:
            print(f"[EmailNotifier] Ошибка отправки email: {e}")