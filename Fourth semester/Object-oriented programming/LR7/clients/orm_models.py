from sqlalchemy import Column, String, Float, Boolean, Enum as SAEnum, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime

def _gen_uuid():
    return str(uuid.uuid4())

class UserORM(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=_gen_uuid)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(SAEnum("customer", "admin", "courier", name="userrole"), default="customer")

class MenuItemORM(Base):
    __tablename__ = "menu_items"
    id = Column(String(36), primary_key=True, default=_gen_uuid)
    restaurant_id = Column(String(36))
    name = Column(String)
    price = Column(Float)
    is_available = Column(Boolean, default=True)

class OrderItemORM(Base):
    __tablename__ = "order_items"
    id = Column(String(36), primary_key=True, default=_gen_uuid)
    order_id = Column(String(36), ForeignKey("orders.id"))
    menu_item_id = Column(String(36))
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer, default=1)
    order = relationship("OrderORM", back_populates="items")

class OrderORM(Base):
    __tablename__ = "orders"
    id = Column(String(36), primary_key=True, default=_gen_uuid)
    customer_id = Column(String(36))
    status = Column(SAEnum("created", "accepted", "preparing", "on_the_way", "delivered", name="orderstatus"), default="created")
    total_price = Column(Float, default=0.0)
    courier_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("OrderItemORM", back_populates="order", cascade="all, delete-orphan")

class CourierORM(Base):
    __tablename__ = "couriers"
    id = Column(String(36), primary_key=True, default=_gen_uuid)
    user_id = Column(String(36), unique=True)
    status = Column(SAEnum("free", "busy", name="courierstatus"), default="free")
    current_order_id = Column(String(36), nullable=True)