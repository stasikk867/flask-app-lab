import pytest

from app import create_app
from app.extensions import db
from app.posts.models import Post


@pytest.fixture
def client():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

        with app.test_client() as client:
            yield client

        db.session.remove()
        db.drop_all()


@pytest.fixture
def post_data():
    return {
        "title": "Test Post",
        "content": "This is a test publication.",
        "publish_date": "2026-11-12T10:30",
        "category": "news",
        "enabled": "y"
    }


def test_posts_list_empty(client):
    response = client.get("/post/")
    assert response.status_code == 200
    assert b"No posts available yet." in response.data


def test_create_post(client, post_data):
    response = client.post("/post/create", data=post_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Post" in response.data

    post = db.session.scalar(
        db.select(Post).where(Post.title == "Test Post")
    )

    assert post is not None
    assert post.author == "Anonymous"
    assert post.is_active is True


def test_post_detail(client, post_data):
    client.post("/post/create", data=post_data)
    post = db.session.scalar(db.select(Post))

    response = client.get(f"/post/{post.id}")

    assert response.status_code == 200
    assert b"Test Post" in response.data


def test_edit_post(client, post_data):
    client.post("/post/create", data=post_data)
    post = db.session.scalar(db.select(Post))

    updated_data = {
        "title": "Updated Post",
        "content": "Updated content.",
        "publish_date": "2026-11-12T12:00",
        "category": "tech",
        "enabled": "y"
    }

    response = client.post(
        f"/post/{post.id}/update",
        data=updated_data,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert db.session.get(Post, post.id).title == "Updated Post"


def test_delete_post(client, post_data):
    client.post("/post/create", data=post_data)
    post = db.session.scalar(db.select(Post))

    response = client.post(
        f"/post/{post.id}/delete",
        data={"submit": "Confirm deletion"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert db.session.get(Post, post.id) is None


def test_post_not_found(client):
    response = client.get("/post/999")
    assert response.status_code == 404


def test_inactive_post_not_in_list(client, post_data):
    post_data.pop("enabled")
    client.post("/post/create", data=post_data)

    response = client.get("/post/")

    assert response.status_code == 200
    assert b"Test Post" not in response.data


def test_invalid_post(client):
    response = client.post(
        "/post/create",
        data={
            "title": "",
            "content": "",
            "publish_date": "2026-11-12T10:30",
            "category": "news"
        }
    )

    assert response.status_code == 200
    assert db.session.scalar(db.select(Post)) is None
