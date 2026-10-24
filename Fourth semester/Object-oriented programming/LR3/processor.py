# =========================================================
# Файл: processor.py
# Описание: Основная бизнес-логика.
# =========================================================
from typing import List

from LR3.notifications import NotificationService
from services import PricingService
from infrastructure import Database
from cache import OrderCache
from models import Order


class OrderProcessor:
    def __init__(
        self,
        database: Database,
        pricing_service: PricingService,
        notifications: List[NotificationService],
        cache: OrderCache,
    ) -> None:
        self.database = database
        self.pricing_service = pricing_service
        self._notifications = notifications
        self._cache = cache

    def Process(self, order: Order) -> None:
        print(f"--- Processing Order {order.id} ---")

        # 0. Проверка кэша
        if self._cache.is_cached(order.id):
            print(f"Order {order.id} already in cache. Skipping.")
            message = f"Order {order.id} already processed (cached)"
            for service in self._notifications:
                service.send(message)
            return

        # 1. Валидация. Вынесли в отдельный метод(SRP)
        self._validate_order(order)

        # 2. Логика расчета суммы
        total = self.pricing_service.calculate_total(order)

        # 3. Логика сохранения
        self.database.save_order(order, total)
        self._cache.add(order.id)

        # 4. Логика уведомлений
        message = f"Your Order {order.id} confirmed. Total: {total:.2f}"
        for service in self._notifications:
            service.send(message)

    def _validate_order(self, order: Order) -> None:
        """Вынос валидации в отдельный метод."""
        if len(order.items) == 0:
            raise ValueError("order must have at least one item")
        if order.destination.city == "":
            raise ValueError("destination city is required")
