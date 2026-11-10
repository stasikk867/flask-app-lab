from app import create_app


def test_contact_page():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert "Зворотний зв'язок".encode("utf-8") in response.data


def test_contact_form_valid_data():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    client = app.test_client()

    response = client.post("/", data={
        "name": "Танасій",
        "email": "test@example.com",
        "phone": "+380123456789",
        "subject": "question",
        "message": "Тестове повідомлення"
    })

    assert response.status_code == 302


def test_contact_form_invalid_email():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    client = app.test_client()

    response = client.post("/", data={
        "name": "Танасій",
        "email": "invalid-email",
        "phone": "+380123456789",
        "subject": "question",
        "message": "Тестове повідомлення"
    })

    assert response.status_code == 200
    assert "коректну email-адресу".encode("utf-8") in response.data