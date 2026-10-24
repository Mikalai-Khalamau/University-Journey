import pytest
from uuid import uuid4
from models import Order, OrderItem, OrderStatus, Courier, CourierStatus, MenuItem

def test_order_calculates_total_correctly():
    item1 = OrderItem(menu_item_id=uuid4(), name="Pizza", price=10.0, quantity=2)
    item2 = OrderItem(menu_item_id=uuid4(), name="Soda", price=2.5, quantity=3)
    order = Order(customer_id=uuid4(), items=[item1, item2])
    assert order.total_price == pytest.approx(27.5)

def test_order_status_transitions():
    order = Order(customer_id=uuid4())
    assert order.status == OrderStatus.CREATED
    assert order.can_transition_to(OrderStatus.ACCEPTED) is True
    assert order.can_transition_to(OrderStatus.PREPARING) is False

    order.status = OrderStatus.ACCEPTED
    assert order.can_transition_to(OrderStatus.PREPARING) is True
    assert order.can_transition_to(OrderStatus.DELIVERED) is False

def test_courier_assignment_and_completion():
    courier = Courier(user_id=uuid4())
    assert courier.is_available is True

    order_id = uuid4()
    courier.assign_order(order_id)
    assert courier.is_available is False
    assert courier.current_order_id == order_id

    with pytest.raises(RuntimeError, match="already busy"):
        courier.assign_order(uuid4())

    courier.complete_order()
    assert courier.is_available is True
    assert courier.current_order_id is None

def test_invalid_menu_item_raises_error():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        MenuItem(name="Test", price=-5.0)
    with pytest.raises(ValueError, match="Name cannot be empty"):
        MenuItem(name="", price=10.0)