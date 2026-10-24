import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from clients.database import Base
from clients.repositories import UserRepository, MenuItemRepository, OrderRepository
from models import User, UserRole, Order, OrderItem, OrderStatus, MenuItem
import uuid

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_user_repository_save_and_fetch(db_session):
    repo = UserRepository(db_session)
    user = User(email="test@food.com", hashed_password="hash123", role=UserRole.CUSTOMER)
    repo.save(user)
    fetched = repo.get_by_email("test@food.com")
    assert fetched is not None
    assert fetched.email == user.email
    assert fetched.role == UserRole.CUSTOMER

def test_menu_item_repository(db_session):
    repo = MenuItemRepository(db_session)
    item = MenuItem(name="Burger", price=5.5, is_available=True)
    repo.save(item)
    items = repo.get_all_available()
    assert len(items) == 1
    assert items[0].name == "Burger"
    assert items[0].price == pytest.approx(5.5)

def test_order_repository_with_items(db_session):
    repo = OrderRepository(db_session)
    order = Order(
        customer_id=uuid.uuid4(),
        items=[OrderItem(menu_item_id=uuid.uuid4(), name="Fries", price=2.0, quantity=3)],
        status=OrderStatus.CREATED
    )
    repo.save(order)
    fetched = repo.get_by_id(order.id)
    assert fetched is not None
    assert fetched.total_price == pytest.approx(6.0)
    assert len(fetched.items) == 1
    assert fetched.items[0].quantity == 3