from uuid import UUID
from typing import List
from .protocols import (
    OrderRepositoryProtocol, CourierRepositoryProtocol,
    MenuItemRepositoryProtocol, UserRepositoryProtocol
)
from shared.exceptions import NotFoundError, BusinessRuleError, AuthError
from shared import OrderItemInput
from models import Order, OrderItem, OrderStatus, User, UserRole, MenuItem, Courier, CourierStatus
from passlib.context import CryptContext
from jose import jwt

class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepositoryProtocol):
        self.order_repo = order_repo

    def execute(self, customer_id: UUID, items: List[OrderItemInput]) -> Order:
        order_items = [
            OrderItem(menu_item_id=i.menu_item_id, name=i.name, price=i.price, quantity=i.quantity)
            for i in items
        ]
        order = Order(customer_id=customer_id, items=order_items)
        self.order_repo.save(order)
        return order

class UpdateOrderStatusUseCase:
    def __init__(self, order_repo: OrderRepositoryProtocol):
        self.order_repo = order_repo

    def execute(self, order_id: UUID, new_status: OrderStatus) -> Order:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundError("Order not found")
        if not order.can_transition_to(new_status):
            raise BusinessRuleError(
                f"Invalid transition: {order.status.value} -> {new_status.value}"
            )
        order.status = new_status
        self.order_repo.save(order)
        return order

class AssignCourierUseCase:
    def __init__(self, order_repo: OrderRepositoryProtocol, courier_repo: CourierRepositoryProtocol):
        self.order_repo = order_repo
        self.courier_repo = courier_repo

    def execute(self, order_id: UUID) -> Order:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundError("Order not found")
        if order.status not in (OrderStatus.ACCEPTED, OrderStatus.PREPARING):
            raise BusinessRuleError("Order must be ACCEPTED or PREPARING")
        if order.courier_id is not None:
            raise BusinessRuleError("Courier already assigned")

        courier = self.courier_repo.get_free()
        if not courier:
            raise BusinessRuleError("No available couriers")

        courier.assign_order(order.id)
        self.courier_repo.save(courier)

        order.assign_courier(courier.id)
        self.order_repo.save(order)
        return order

class GetMenuUseCase:
    def __init__(self, menu_repo: MenuItemRepositoryProtocol):
        self.menu_repo = menu_repo

    def execute(self) -> List[MenuItem]:
        return self.menu_repo.get_all_available()

class RegisterUseCase:
    def __init__(self, repo: UserRepositoryProtocol):
        self.repo = repo

    def execute(self, email: str, password: str) -> User:

        pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if self.repo.get_by_email(email):
            raise BusinessRuleError("User already exists")
        user = User(email=email, hashed_password=pwd_ctx.hash(password), role=UserRole.CUSTOMER)
        self.repo.save(user)
        return user

    def generate_token(self, user_id: UUID, role: str) -> str:
        return jwt.encode({"sub": str(user_id), "role": role}, "lab_secret_key", algorithm="HS256")

class LoginUseCase:
    def __init__(self, repo: UserRepositoryProtocol):
        self.repo = repo

    def execute(self, email: str, password: str) -> str:
        pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user = self.repo.get_by_email(email)
        if not user or not pwd_ctx.verify(password, user.hashed_password):
            raise AuthError("Invalid credentials")
        return jwt.encode({"sub": str(user.id), "role": user.role.value}, "lab_secret_key", algorithm="HS256")


class CreateMenuItemUseCase:

    def __init__(self, menu_repo: MenuItemRepositoryProtocol):
        self.menu_repo = menu_repo

    def execute(self, restaurant_id: UUID, name: str, price: float, is_available: bool = True) -> MenuItem:
        item = MenuItem(
            restaurant_id=restaurant_id,
            name=name,
            price=price,
            is_available=is_available
        )
        self.menu_repo.save(item)
        return item

class RegisterCourierUseCase:

    def __init__(self, user_repo: UserRepositoryProtocol, courier_repo: CourierRepositoryProtocol):
        self.user_repo = user_repo
        self.courier_repo = courier_repo

    def execute(self, email: str, password: str) -> Courier:
        pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

        if self.user_repo.get_by_email(email):
            raise BusinessRuleError("User already exists")

        user = User(email=email, hashed_password=pwd_ctx.hash(password), role=UserRole.COURIER)
        self.user_repo.save(user)

        courier = Courier(user_id=user.id, status=CourierStatus.FREE)
        self.courier_repo.save(courier)

        return courier