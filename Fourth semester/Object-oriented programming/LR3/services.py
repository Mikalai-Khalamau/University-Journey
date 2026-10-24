from abc import ABC, abstractmethod

from models import OrderType
from models import Order, DiscountCardType


class TaxStrategy(ABC):
    """Стратегия расчета налогов."""

    @abstractmethod
    def calculate(self, base_total: float, order: Order) -> float:
        pass


class StandardTax(TaxStrategy):
    def calculate(self, base_total: float, order: Order) -> float:
        return base_total * 1.2


class PremiumTax(TaxStrategy):
    def calculate(self, base_total: float, order: Order) -> float:
        return (base_total * 0.9) * 1.2


class BudgetTax(TaxStrategy):
    def calculate(self, base_total: float, order: Order) -> float:
        if len(order.items) > 3:
            raise ValueError("Budget orders cannot have more than 3 items. Skipping.")
        return base_total


class InternationalTax(TaxStrategy):
    def calculate(self, base_total: float, order: Order) -> float:
        if order.destination.city == "Nowhere":
            raise ValueError("cannot ship to Nowhere")
        return base_total * 1.5


class PricingService:
    """Сервис расчета итоговой цены."""

    def __init__(self):
        self._tax_strategies = {
            OrderType.STANDARD: StandardTax(),
            OrderType.PREMIUM: PremiumTax(),
            OrderType.BUDGET: BudgetTax(),
            OrderType.INTERNATIONAL: InternationalTax(),
        }
        self._discount_service = DiscountService()

    def calculate_total(self, order: Order) -> float:
        if order is None:
            raise ValueError("Order cannot be None")
        if not order.items:
            raise ValueError("Order must have items")
        base_price = sum(item.price for item in order.items)

        strategy = self._tax_strategies.get(order.type)
        if strategy is None:
            raise ValueError("Unknown order type")
        total_with_tax = strategy.calculate(base_price, order)

        discount_strategy = self._discount_service.get_discount(order.discount_card)
        discount = total_with_tax * discount_strategy.get_discount_percent()
        return total_with_tax - discount


class DiscountStrategy(ABC):
    """Стратегия расчёта скидки (OCP)"""

    @abstractmethod
    def get_discount_percent(self) -> float:
        """Вернуть процент скидки (0.0 - 1.0)"""
        pass


class NewbieDiscount(DiscountStrategy):
    def get_discount_percent(self) -> float:
        return 0.0


class SilverDiscount(DiscountStrategy):
    def get_discount_percent(self) -> float:
        return 0.10


class GoldDiscount(DiscountStrategy):
    def get_discount_percent(self) -> float:
        return 0.15


class DiscountService:
    """Сервис применения скидок"""

    def __init__(self):
        self._strategies = {
            DiscountCardType.NEWBIE: NewbieDiscount(),
            DiscountCardType.SILVER: SilverDiscount(),
            DiscountCardType.GOLD: GoldDiscount(),
        }

    def get_discount(self, card_type: DiscountCardType) -> DiscountStrategy:
        return self._strategies.get(card_type, NewbieDiscount())
