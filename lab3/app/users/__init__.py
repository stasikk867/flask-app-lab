from flask import Blueprint

users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/hi",
    template_folder="templates"
)

from . import views