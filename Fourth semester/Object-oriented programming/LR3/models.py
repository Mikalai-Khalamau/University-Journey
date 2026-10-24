# =========================================================
# Файл: models.py
# Описание: Модели данных системы.
# =========================================================
from typing import List
from enum import Enum


class OrderType(Enum):
    STANDARD = "Standard"
    PREMIUM = "Premium"
    BUDGET = "Budget"
    INTERNATIONAL = "International"


class DiscountCardType(Enum):
    """Типы дисконтных карт"""

    NEWBIE = "Newbie"
    SILVER = "Silver"
    GOLD = "Gold"


# Item - товар в заказе
class Item:
    id: str
    name: str
    price: float

    def __init__(self, id: str, name: str, price: float) -> None:
        if not id:
            raise ValueError("Id is required")
        if price < 0:
            raise ValueError("Price can not be negative")
        self.id = id
        self.name = name
        self.price = price


# Address - адрес доставки
class Address:
    city: str
    street: str
    zip: str

    def __init__(self, city: str, street: str, zip: str) -> None:
        if not city:
            raise ValueError("City is required")
        if not street:
            raise ValueError("Street is required")
        self.city = city
        self.street = street
        self.zip = zip


# Order - заказ
class Order:
    id: str
    items: List[Item]
    type: OrderType  # "Standard", "Premium", "Budget", "International"
    client_email: str
    user: str
    destination: Address

    def __init__(
        self,
        id: str,
        items: List[Item],
        type: OrderType,
        client_email: str,
        user: str,
        destination: Address,
        discount_card: DiscountCardType = DiscountCardType.NEWBIE,
    ):
        if not id:
            raise ValueError("Order must have an ID")

        if not items:
            raise ValueError("Order must have at least one item")

        if not client_email or "@" not in client_email:
            raise ValueError(f"Invalid client email: {client_email}")

        self.id = id
        self.items = items
        self.type = type
        self.client_email = client_email
        self.user = user
        self.destination = destination
        self.discount_card = discount_card
