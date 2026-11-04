
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


def test_product_list_empty(client):
    response = client.get("/products/")

    assert response.status_code == 200
    assert "Товарів поки немає".encode("utf-8") in response.data


def test_create_product(client):
    response = client.post("/products/create", data={
        "name": "Ноутбук",
        "price": "25000",
        "description": "Ноутбук для навчання"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Ноутбук".encode("utf-8") in response.data


def test_product_detail(client):
    client.post("/products/create", data={
        "name": "Телефон",
        "price": "15000",
        "description": "Смартфон"
    })

    response = client.get("/products/1")

    assert response.status_code == 200
    assert "Телефон".encode("utf-8") in response.data


def test_edit_product(client):
    client.post("/products/create", data={
        "name": "Ноутбук",
        "price": "25000",
        "description": "Старий опис"
    })

    response = client.post("/products/1/edit", data={
        "name": "Новий ноутбук",
        "price": "30000",
        "description": "Новий опис"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Новий ноутбук".encode("utf-8") in response.data
    assert "30000".encode("utf-8") in response.data


def test_delete_product(client):
    client.post("/products/create", data={
        "name": "Навушники",
        "price": "3000",
        "description": "Бездротові навушники"
    })

    response = client.post(
        "/products/1/delete",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Товарів поки немає".encode("utf-8") in response.data


def test_product_not_found(client):
    response = client.get("/products/999")

    assert response.status_code == 404
