from fastapi import Depends
from clients.database import SessionLocal
from clients.repositories import UserRepository, OrderRepository, CourierRepository, MenuItemRepository
from controllers.use_cases import (
    CreateOrderUseCase, UpdateOrderStatusUseCase, AssignCourierUseCase,
    GetMenuUseCase, RegisterUseCase, LoginUseCase, CreateMenuItemUseCase, RegisterCourierUseCase
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repo(db=Depends(get_db)): return UserRepository(db)
def get_order_repo(db=Depends(get_db)): return OrderRepository(db)
def get_courier_repo(db=Depends(get_db)): return CourierRepository(db)
def get_menu_repo(db=Depends(get_db)): return MenuItemRepository(db)

def get_register_use_case(repo=Depends(get_user_repo)): return RegisterUseCase(repo)
def get_login_use_case(repo=Depends(get_user_repo)): return LoginUseCase(repo)
def get_create_order_use_case(repo=Depends(get_order_repo)): return CreateOrderUseCase(repo)
def get_update_status_use_case(repo=Depends(get_order_repo)): return UpdateOrderStatusUseCase(repo)
def get_assign_courier_use_case(order_repo=Depends(get_order_repo), courier_repo=Depends(get_courier_repo)):
    return AssignCourierUseCase(order_repo, courier_repo)
def get_menu_use_case(repo=Depends(get_menu_repo)): return GetMenuUseCase(repo)

def get_create_menu_item_use_case(repo=Depends(get_menu_repo)):
    return CreateMenuItemUseCase(repo)

def get_register_courier_use_case(
    user_repo=Depends(get_user_repo),
    courier_repo=Depends(get_courier_repo)
):
    return RegisterCourierUseCase(user_repo, courier_repo)