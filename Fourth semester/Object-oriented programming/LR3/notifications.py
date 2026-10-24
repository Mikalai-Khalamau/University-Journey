from abc import ABC, abstractmethod


class NotificationService(ABC):
    """Абстракция уведомлений"""

    @abstractmethod
    def send(self, message: str) -> None:
        """Отправить уведомление"""
        pass


class EmailNotification(NotificationService):
    def __init__(self, email: str, smtp_server: str = "smtp.gmail.com"):
        if not smtp_server:
            raise ValueError("SMTP server is required")
        if not email:
            raise ValueError("Recipient email is required")
        if "@" not in email:
            raise ValueError(f"Invalid recipient email: {email}")

        self.email = email
        self.smtp_server = smtp_server

    def send(self, message: str) -> None:
        if not message:
            raise ValueError("Email body is required")

        print(f">> Connecting to SMTP server {self.smtp_server}...")
        print(f">> Sending EMAIL to {self.email}")
        print(f"   Body: {message}")


class TelegramNotification(NotificationService):
    def __init__(self, user: str):
        self.user = user

    def send(self, message: str) -> None:
        print(f"Telegram to manager {self.user}: {message}")


class LogNotification(NotificationService):
    def __init__(self, filename: str = "notifications.log"):
        self.filename = filename

    def send(self, message: str) -> None:
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(f"{message}\n")
        print(f"Log: {message}")
