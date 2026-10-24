# =========================================================
# Файл: infrastructure.py
# Описание: Имитация работы с БД и внешними сервисами.
# =========================================================
import time
from abc import ABC, abstractmethod
from datetime import datetime
from models import Order


class Database(ABC):
    """Абстракция базы данных."""

    @abstractmethod
    def save_order(self, order: Order, total: float) -> None:
        pass


# RandomSQLDatabase - имитация тяжелой базы данных
class RandomSQLDatabase(Database):
    def __init__(self):
        self.connection_string = "random://root:password@localhost:228/shop"

    # Сохранение заказа в "базу данных"
    def save_order(self, order: Order, total: float) -> None:
        if order is None:
            raise ValueError("Order cannot be None")
        if total < 0:
            raise ValueError(f"Total cannot be negative: {total}")
        print(f"Connecting to RandomSQL at {self.connection_string} ...")
        time.sleep(0.5)  # Имитация задержки сети

        with open("orders_db.txt", "a") as file:
            record = f"[{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}] ID: {order.id} | Type: {order.type} | Total: {total:.2f}\n"
            file.write(record)

        print("Order saved successfully.")
