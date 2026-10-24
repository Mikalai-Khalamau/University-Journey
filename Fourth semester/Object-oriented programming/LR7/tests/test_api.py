from fastapi.testclient import TestClient
from main import app
from clients.database import engine
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    from clients.database import Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_auth_flow():
    r = client.post("/api/v1/auth/register", json={"email": "test_auth@lab.com", "password": "123456"})
    assert r.status_code == 200, f"Register failed: {r.json()}"
    token = r.json()["access_token"]
    assert token is not None

    r = client.post("/api/v1/auth/login", json={"email": "test_auth@lab.com", "password": "123456"})
    assert r.status_code == 200, f"Login failed: {r.json()}"

def test_menu_endpoint():
    r = client.get("/api/v1/menu")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_create_and_update_order():
    order_req = {
        "items": [{
            "menu_item_id": "00000000-0000-0000-0000-000000000001",
            "name": "Burger",
            "price": 10.0,
            "quantity": 2
        }]
    }
    r = client.post("/api/v1/orders", json=order_req)
    assert r.status_code == 200, f"Create order failed: {r.json()}"
    order_id = r.json()["id"]

    r = client.patch(f"/api/v1/orders/{order_id}/status", json={"status": "accepted"})
    assert r.status_code == 200, f"Update status failed: {r.json()}"
    assert r.json()["status"] == "accepted"

    r = client.patch(f"/api/v1/orders/{order_id}/status", json={"status": "delivered"})
    assert r.status_code == 400


def test_create_menu_item():
    menu_item_data = {
        "restaurant_id": "00000000-0000-0000-0000-000000000001",
        "name": "Test Pizza",
        "price": 12.5,
        "is_available": True
    }
    r = client.post("/api/v1/menu", json=menu_item_data)
    assert r.status_code == 200, f"Create menu item failed: {r.json()}"
    item = r.json()
    assert item["name"] == "Test Pizza"
    assert item["price"] == 12.5


def test_register_courier():
    courier_data = {
        "email": "courier@food.com",
        "password": "123456"
    }
    r = client.post("/api/v1/couriers", json=courier_data)
    assert r.status_code == 200, f"Register courier failed: {r.json()}"
    courier = r.json()
    assert courier["status"] == "free"


def test_full_order_with_courier():
    # 1. Создаём блюдо
    menu_item_data = {
        "restaurant_id": "00000000-0000-0000-0000-000000000001",
        "name": "Full Test Burger",
        "price": 10.0,
        "is_available": True
    }
    r = client.post("/api/v1/menu", json=menu_item_data)
    assert r.status_code == 200
    menu_item = r.json()

    # 2. Регистрируем курьера
    courier_data = {"email": "fulltest@courier.com", "password": "123456"}
    r = client.post("/api/v1/couriers", json=courier_data)
    assert r.status_code == 200

    # 3. Создаём заказ с реальным блюдом из меню
    order_req = {
        "items": [{
            "menu_item_id": menu_item["id"],
            "name": menu_item["name"],
            "price": menu_item["price"],
            "quantity": 3
        }]
    }
    r = client.post("/api/v1/orders", json=order_req)
    assert r.status_code == 200
    order = r.json()
    assert order["total_price"] == 30.0
    order_id = order["id"]

    # 4. Меняем статусы
    r = client.patch(f"/api/v1/orders/{order_id}/status", json={"status": "accepted"})
    assert r.status_code == 200

    r = client.patch(f"/api/v1/orders/{order_id}/status", json={"status": "preparing"})
    assert r.status_code == 200

    # 5. Назначаем курьера
    r = client.post(f"/api/v1/orders/{order_id}/courier")
    assert r.status_code == 200, f"Assign courier failed: {r.json()}"
    result = r.json()
    assert result["order_id"] == order_id
    assert result["courier_id"] is not None