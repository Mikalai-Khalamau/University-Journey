from fastapi import APIRouter, Depends, HTTPException, status
from . import schemas, dependencies
from controllers import (
    RegisterUseCase, LoginUseCase, CreateOrderUseCase, UpdateOrderStatusUseCase,
    AssignCourierUseCase, GetMenuUseCase, CreateMenuItemUseCase, RegisterCourierUseCase
)
from shared.exceptions import NotFoundError, BusinessRuleError, AuthError
from shared import OrderItemInput

router = APIRouter()

@router.post("/auth/register", response_model=schemas.TokenResponse, tags=["Auth"])
def register(req: schemas.RegisterRequest, uc: RegisterUseCase = Depends(dependencies.get_register_use_case)):
    try:
        user = uc.execute(req.email, req.password)
        token = uc.generate_token(user.id, user.role.value)
        return schemas.TokenResponse(access_token=token)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

@router.post("/auth/login", response_model=schemas.TokenResponse, tags=["Auth"])
def login(req: schemas.LoginRequest, uc: LoginUseCase = Depends(dependencies.get_login_use_case)):
    try:
        return schemas.TokenResponse(access_token=uc.execute(req.email, req.password))
    except AuthError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")


@router.get("/menu", response_model=list[schemas.MenuItemResponse], tags=["Menu"])
def get_menu(uc: GetMenuUseCase = Depends(dependencies.get_menu_use_case)):
    return uc.execute()

@router.post("/menu", response_model=schemas.MenuItemResponse, tags=["Menu"])
def create_menu_item(
    req: schemas.CreateMenuItemRequest,
    uc: CreateMenuItemUseCase = Depends(dependencies.get_create_menu_item_use_case)
):
    """Добавить новое блюдо в меню."""
    return uc.execute(
        restaurant_id=req.restaurant_id,
        name=req.name,
        price=req.price,
        is_available=req.is_available
    )

@router.post("/orders", response_model=schemas.OrderResponse, tags=["Orders"])
def create_order(req: schemas.CreateOrderRequest, uc: CreateOrderUseCase = Depends(dependencies.get_create_order_use_case)):
    from uuid import UUID
    customer_id = UUID("00000000-0000-0000-0000-000000000000")
    items = [OrderItemInput(**i.model_dump()) for i in req.items]
    return uc.execute(customer_id=customer_id, items=items)

@router.patch("/orders/{order_id}/status", response_model=schemas.OrderResponse, tags=["Orders"])
def update_status(order_id: str, req: schemas.UpdateOrderStatusRequest, uc: UpdateOrderStatusUseCase = Depends(dependencies.get_update_status_use_case)):
    try:
        return uc.execute(order_id, req.status)
    except NotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(NotFoundError("Order not found")))
    except BusinessRuleError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(BusinessRuleError("Invalid status transition")))

@router.post("/orders/{order_id}/courier", response_model=schemas.AssignCourierResponse, tags=["Orders"])
def assign_courier(order_id: str, uc: AssignCourierUseCase = Depends(dependencies.get_assign_courier_use_case)):
    try:
        order = uc.execute(order_id)
        return schemas.AssignCourierResponse(order_id=order.id, courier_id=order.courier_id)
    except NotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")
    except BusinessRuleError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(BusinessRuleError("Cannot assign courier")))

@router.post("/couriers", response_model=schemas.CourierResponse, tags=["Couriers"])
def register_courier(
    req: schemas.CreateCourierRequest,
    uc: RegisterCourierUseCase = Depends(dependencies.get_register_courier_use_case)
):
    """Зарегистрировать нового курьера."""
    return uc.execute(email=req.email, password=req.password)

@router.get("/couriers/free", response_model=list[schemas.CourierResponse], tags=["Couriers"])
def get_free_couriers(courier_repo=Depends(dependencies.get_courier_repo)):
    """Получить список свободных курьеров."""
    free_courier = courier_repo.get_free()
    return [free_courier] if free_courier else []