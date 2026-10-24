# =========================================================
# Файл: main.py
# Описание: Точка входа в приложение.
# =========================================================
import sys

from notifications import EmailNotification, TelegramNotification, LogNotification
from models import OrderType
from infrastructure import RandomSQLDatabase
from services import PricingService
from models import Address, Item, Order, DiscountCardType
from processor import OrderProcessor
from staff import HumanManager, RobotPacker, WarehouseWorker, manage_warehouse
from cache import InMemoryOrderCache, CacheManager, LRUStrategy, FIFOStrategy, LFUStrategy


def main():
    # 1. Создание заказа
    order = Order(
        id="ORD-256-X",
        type=OrderType.PREMIUM,
        items=[
            Item(id="1", name="Thermal Clips", price=1500),
            Item(id="2", name="UNATCO Pass Card", price=50),
        ],
        client_email="jeevacation@gmail.com",
        user="Manager-Aleksandr",
        destination=Address(
            city="Agartha", street="33 Thomas Street", zip="[REDACTED]"
        ),
        discount_card=DiscountCardType.GOLD,
    )

    # 2. Инициализация процессора
    notifications = [
        EmailNotification(order.client_email),
        TelegramNotification(order.user),
        LogNotification(),
    ]

    cache = CacheManager.create_cache(strategy_name='lru', max_size=5)

    database = RandomSQLDatabase()
    pricing_service = PricingService()
    processor = OrderProcessor(database, pricing_service, notifications, cache)

    print("Processing order...")
    # 3. Обработка заказа
    try:
        processor.Process(order)
    except Exception as e:
        print(f"Failed to process order: {e}", file=sys.stderr)
        sys.exit(1)

    # Сработает ошибка кэша

    processor.Process(order)

    # 4. Работа с обслуживанием
    print("\nTesting Warehouse Stuff:")
    workers: list[WarehouseWorker] = [
        HumanManager(),
        RobotPacker(model="George Droid"),
    ]
    manage_warehouse(workers)


if __name__ == "__main__":

    main()
