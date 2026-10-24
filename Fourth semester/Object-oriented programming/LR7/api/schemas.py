from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from models import OrderStatus, CourierStatus


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MenuItemResponse(BaseModel):
    id: UUID
    restaurant_id: UUID
    name: str
    price: float
    is_available: bool
    model_config = {"from_attributes": True}

class OrderItemCreate(BaseModel):
    menu_item_id: UUID
    name: str
    price: float
    quantity: int = Field(..., ge=1)

class CreateOrderRequest(BaseModel):
    items: List[OrderItemCreate]

class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus

class OrderItemResponse(BaseModel):
    menu_item_id: UUID
    name: str
    price: float
    quantity: int
    model_config = {"from_attributes": True}

class OrderResponse(BaseModel):
    id: UUID
    customer_id: UUID
    items: List[OrderItemResponse]
    status: OrderStatus
    total_price: float
    courier_id: Optional[UUID] = None
    created_at: datetime
    model_config = {"from_attributes": True}

class AssignCourierResponse(BaseModel):
    order_id: UUID
    courier_id: UUID
    model_config = {"from_attributes": True}

class CreateMenuItemRequest(BaseModel):
    restaurant_id: UUID
    name: str
    price: float = Field(..., ge=0)
    is_available: bool = True

class CreateCourierRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class CourierResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: CourierStatus
    current_order_id: Optional[UUID] = None
    model_config = {"from_attributes": True}