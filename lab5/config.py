import os


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "lab5-development-secret-key"
    )

    WTF_CSRF_ENABLED = True

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__),
        "app",
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}