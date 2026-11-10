import pytest
from tinydb import TinyDB

from app import create_app
import app.products.routes as product_routes


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "products.json"

    def test_get_db():
        return TinyDB(db_path)

    monkeypatch.setattr(product_routes, "get_db", test_get_db)

    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["UPLOAD_FOLDER"] = str(tmp_path / "uploads")

    with app.test_client() as client:
        yield client


@pytest.fixture
def product_data():
    return {
        "name": "Ноутбук",
        "content": "Ноутбук для навчання",
        "price": "25000.00",
        "category": "electronics",
        "quantity": "5"
    }


def test_product_list_empty(client):
    response = client.get("/product/")

    assert response.status_code == 200
    assert "Товарів поки немає".encode("utf-8") in response.data


def test_create_product(client, product_data):
    response = client.post(
        "/product/add",
        data=product_data,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Ноутбук".encode("utf-8") in response.data
    assert "25000.00".encode("utf-8") in response.data

    db = product_routes.get_db()
    product = db.table("products").get(doc_id=1)

    assert product is not None
    assert product["id"] == 1
    assert product["name"] == "Ноутбук"
    assert product["content"] == "Ноутбук для навчання"
    assert product["price"] == 25000.0
    assert product["category"] == "electronics"
    assert product["quantity"] == 5
    assert product["created_at"]

    db.close()


def test_product_detail(client, product_data):
    client.post("/product/add", data=product_data)

    response = client.get("/product/1")

    assert response.status_code == 200
    assert "Ноутбук".encode("utf-8") in response.data
    assert "Ноутбук для навчання".encode("utf-8") in response.data
    assert "electronics".encode("utf-8") in response.data


def test_edit_product(client, product_data):
    client.post("/product/add", data=product_data)

    db = product_routes.get_db()
    original = db.table("products").get(doc_id=1)
    original_created_at = original["created_at"]
    db.close()

    updated_data = {
        "name": "Новий ноутбук",
        "content": "Оновлений опис",
        "price": "30000.00",
        "category": "electronics",
        "quantity": "10"
    }

    response = client.post(
        "/product/1/edit",
        data=updated_data,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Новий ноутбук".encode("utf-8") in response.data
    assert "Оновлений опис".encode("utf-8") in response.data

    db = product_routes.get_db()
    updated = db.table("products").get(doc_id=1)

    assert updated["id"] == 1
    assert updated["price"] == 30000.0
    assert updated["quantity"] == 10
    assert updated["created_at"] == original_created_at

    db.close()


def test_delete_product(client, product_data):
    client.post("/product/add", data=product_data)

    response = client.post(
        "/product/1/delete",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Товарів поки немає".encode("utf-8") in response.data


def test_product_not_found(client):
    response = client.get("/product/999")

    assert response.status_code == 404


def test_product_invalid_price(client, product_data):
    product_data["price"] = "0"

    response = client.post("/product/add", data=product_data)

    assert response.status_code == 200

    db = product_routes.get_db()
    assert db.table("products").all() == []
    db.close()


def test_product_invalid_quantity(client, product_data):
    product_data["quantity"] = "-5"

    response = client.post("/product/add", data=product_data)

    assert response.status_code == 200

    db = product_routes.get_db()
    assert db.table("products").all() == []
    db.close()

