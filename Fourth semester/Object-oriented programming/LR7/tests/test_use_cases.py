import pytest
from unittest.mock import Mock
from uuid import uuid4
from controllers import CreateOrderUseCase, UpdateOrderStatusUseCase, AssignCourierUseCase
from models import Order, OrderStatus, Courier, CourierStatus
from shared.exceptions import NotFoundError, BusinessRuleError
from shared import OrderItemInput

def test_create_order_use_case():
    mock_repo = Mock()
    use_case = CreateOrderUseCase(order_repo=mock_repo)
    customer_id = uuid4()
    items = [OrderItemInput(menu_item_id=uuid4(), name="Burger", price=10.0, quantity=2)]

    order = use_case.execute(customer_id, items)

    assert order.customer_id == customer_id
    assert order.total_price == pytest.approx(20.0)
    mock_repo.save.assert_called_once()

def test_update_status_valid_transition():
    mock_repo = Mock()
    existing_order = Order(customer_id=uuid4(), status=OrderStatus.CREATED)
    mock_repo.get_by_id.return_value = existing_order

    use_case = UpdateOrderStatusUseCase(order_repo=mock_repo)
    updated = use_case.execute(existing_order.id, OrderStatus.ACCEPTED)

    assert updated.status == OrderStatus.ACCEPTED
    mock_repo.save.assert_called_once()

def test_update_status_invalid_transition():
    mock_repo = Mock()
    existing_order = Order(customer_id=uuid4(), status=OrderStatus.CREATED)
    mock_repo.get_by_id.return_value = existing_order

    use_case = UpdateOrderStatusUseCase(order_repo=mock_repo)
    with pytest.raises(BusinessRuleError):
        use_case.execute(existing_order.id, OrderStatus.DELIVERED)

def test_assign_courier_success():
    mock_order_repo = Mock()
    mock_courier_repo = Mock()

    order = Order(customer_id=uuid4(), status=OrderStatus.ACCEPTED)
    mock_order_repo.get_by_id.return_value = order

    courier = Courier(user_id=uuid4(), status=CourierStatus.FREE)
    mock_courier_repo.get_free.return_value = courier

    use_case = AssignCourierUseCase(order_repo=mock_order_repo, courier_repo=mock_courier_repo)
    updated = use_case.execute(order.id)

    assert updated.courier_id == courier.id
    assert mock_courier_repo.save.called
    assert mock_order_repo.save.called

def test_assign_courier_none_available():
    mock_order_repo = Mock()
    mock_courier_repo = Mock()
    mock_order_repo.get_by_id.return_value = Order(customer_id=uuid4(), status=OrderStatus.ACCEPTED)
    mock_courier_repo.get_free.return_value = None

    use_case = AssignCourierUseCase(order_repo=mock_order_repo, courier_repo=mock_courier_repo)
    with pytest.raises(BusinessRuleError, match="No available couriers"):
        use_case.execute(uuid4())