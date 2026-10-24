from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    COURIER = "courier"

class OrderStatus(str, Enum):
    CREATED = "created"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"

class CourierStatus(str, Enum):
    FREE = "free"
    BUSY = "busy"

# Карта допустимых переходов статусов заказа
ALLOWED_ORDER_TRANSITIONS = {
    OrderStatus.CREATED: [OrderStatus.ACCEPTED],
    OrderStatus.ACCEPTED: [OrderStatus.PREPARING],
    OrderStatus.PREPARING: [OrderStatus.ON_THE_WAY],
    OrderStatus.ON_THE_WAY: [OrderStatus.DELIVERED],
}

# Доменные сущности
@dataclass
class MenuItem:
    """Позиция в меню ресторана."""
    id: UUID = field(default_factory=uuid4)
    restaurant_id: UUID = field(default_factory=uuid4)
    name: str = ""
    price: float = 0.0
    is_available: bool = True

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not self.name:
            raise ValueError("Name cannot be empty")

@dataclass
class OrderItem:
    """Позиция в заказе клиента."""
    menu_item_id: UUID
    name: str
    price: float
    quantity: int = 1

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

@dataclass
class Order:
    """Заказ клиента. Инкапсулирует правила расчёта и смены статусов."""
    id: UUID = field(default_factory=uuid4)
    customer_id: UUID = field(default_factory=uuid4)
    items: list[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    total_price: float = 0.0
    courier_id: Optional[UUID] = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self.calculate_total()

    def calculate_total(self) -> float:
        """Пересчитывает итоговую стоимость заказа."""
        self.total_price = sum(item.price * item.quantity for item in self.items)
        return self.total_price

    def can_transition_to(self, new_status: OrderStatus) -> bool:
        """Проверяет, допустим ли переход в новый статус."""
        allowed = ALLOWED_ORDER_TRANSITIONS.get(self.status, [])
        return new_status in allowed

    def assign_courier(self, courier_id: UUID) -> None:
        """Привязывает курьера к заказу."""
        if self.status not in (OrderStatus.ACCEPTED, OrderStatus.PREPARING):
            raise ValueError("Courier can only be assigned to ACCEPTED or PREPARING orders")
        self.courier_id = courier_id

@dataclass
class Courier:
    """Курьер. Управляет состоянием занятости."""
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    status: CourierStatus = CourierStatus.FREE
    current_order_id: Optional[UUID] = None

    @property
    def is_available(self) -> bool:
        return self.status == CourierStatus.FREE

    def assign_order(self, order_id: UUID) -> None:
        if not self.is_available:
            raise RuntimeError("Courier is already busy")
        self.status = CourierStatus.BUSY
        self.current_order_id = order_id

    def complete_order(self) -> None:
        self.status = CourierStatus.FREE
        self.current_order_id = None

@dataclass
class User:
    """Пользователь системы."""
    id: UUID = field(default_factory=uuid4)
    email: str = ""
    hashed_password: str = ""
    role: UserRole = UserRole.CUSTOMER