from sqlalchemy import select
from sqlalchemy.orm import Session
from .orm_models import UserORM, OrderORM, OrderItemORM, CourierORM, MenuItemORM
from models import User, Order, OrderItem, Courier, MenuItem, UserRole, OrderStatus, CourierStatus
import uuid

def _to_uuid(val: str | None) -> uuid.UUID | None:
    return uuid.UUID(val) if val else None

class UserRepository:
    def __init__(self, db: Session): self.db = db
    def get_by_email(self, email: str) -> User | None:
        stmt = select(UserORM).where(UserORM.email == email)
        orm = self.db.execute(stmt).scalar_one_or_none()
        return self._to_domain(orm) if orm else None
    def save(self, user: User) -> None:
        orm = UserORM(id=str(user.id), email=user.email, hashed_password=user.hashed_password, role=user.role.value)
        self.db.merge(orm)
        self.db.commit()
    @staticmethod
    def _to_domain(orm: UserORM) -> User:
        return User(id=uuid.UUID(orm.id), email=orm.email, hashed_password=orm.hashed_password, role=UserRole(orm.role))

class OrderRepository:
    def __init__(self, db: Session): self.db = db
    def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        stmt = select(OrderORM).where(OrderORM.id == str(order_id))
        orm = self.db.execute(stmt).scalar_one_or_none()
        return self._to_domain(orm) if orm else None
    def save(self, order: Order) -> None:
        orm = OrderORM(
            id=str(order.id), customer_id=str(order.customer_id),
            status=order.status.value, total_price=order.total_price,
            courier_id=str(order.courier_id) if order.courier_id else None,
            created_at=order.created_at
        )
        orm.items = [
            OrderItemORM(menu_item_id=str(i.menu_item_id), name=i.name, price=i.price, quantity=i.quantity)
            for i in order.items
        ]
        self.db.merge(orm)
        self.db.commit()
    @staticmethod
    def _to_domain(orm: OrderORM) -> Order:
        return Order(
            id=uuid.UUID(orm.id), customer_id=uuid.UUID(orm.customer_id),
            status=OrderStatus(orm.status), total_price=orm.total_price,
            courier_id=_to_uuid(orm.courier_id), created_at=orm.created_at,
            items=[OrderItem(menu_item_id=uuid.UUID(i.menu_item_id), name=i.name, price=i.price, quantity=i.quantity) for i in orm.items]
        )

class CourierRepository:
    def __init__(self, db: Session): self.db = db
    def get_free(self) -> Courier | None:
        stmt = select(CourierORM).where(CourierORM.status == "free").limit(1)
        orm = self.db.execute(stmt).scalar_one_or_none()
        return self._to_domain(orm) if orm else None
    def save(self, courier: Courier) -> None:
        orm = CourierORM(
            id=str(courier.id), user_id=str(courier.user_id),
            status=courier.status.value,
            current_order_id=str(courier.current_order_id) if courier.current_order_id else None
        )
        self.db.merge(orm)
        self.db.commit()
    @staticmethod
    def _to_domain(orm: CourierORM) -> Courier:
        return Courier(
            id=uuid.UUID(orm.id), user_id=uuid.UUID(orm.user_id),
            status=CourierStatus(orm.status), current_order_id=_to_uuid(orm.current_order_id)
        )

class MenuItemRepository:
    def __init__(self, db: Session): self.db = db
    def get_all_available(self) -> list[MenuItem]:
        stmt = select(MenuItemORM).where(MenuItemORM.is_available == True)
        orms = self.db.execute(stmt).scalars().all()
        return [self._to_domain(orm) for orm in orms]
    def save(self, item: MenuItem) -> None:
        orm = MenuItemORM(id=str(item.id), restaurant_id=str(item.restaurant_id), name=item.name, price=item.price, is_available=item.is_available)
        self.db.merge(orm)
        self.db.commit()
    @staticmethod
    def _to_domain(orm: MenuItemORM) -> MenuItem:
        return MenuItem(id=uuid.UUID(orm.id), restaurant_id=uuid.UUID(orm.restaurant_id), name=orm.name, price=orm.price, is_available=orm.is_available)