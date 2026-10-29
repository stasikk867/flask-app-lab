
from datetime import datetime, timedelta

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    make_response,
)

from . import users_bp


# Тестові дані для входу
USERNAME = "user1"
PASSWORD = "12345"


@users_bp.route("/")
def home():
    return render_template("base.html")


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль.", "error")
        return redirect(url_for("users.login"))

    return render_template("login.html")


@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("theme", "light")
    cookies = request.cookies

    return render_template(
        "profile.html",
        username=session["username"],
        theme=theme,
        cookies=cookies,
    )


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "success")
    return redirect(url_for("users.login"))


@users_bp.route("/add-cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    days = request.form.get("days", "7", type=int)

    if not key:
        flash("Введіть назву cookie.", "error")
        return redirect(url_for("users.profile"))

    if key.lower() in {"username", "session", "theme"}:
        flash("Ця назва cookie зарезервована.", "error")
        return redirect(url_for("users.profile"))

    if days is None or days < 0:
        flash("Термін дії має бути невід’ємним числом.", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    expires = datetime.now() + timedelta(days=days)
    response.set_cookie(key, value, expires=expires)
    flash("Cookie успішно додано.", "success")
    return response


@users_bp.route("/delete-cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()

    if not key:
        flash("Введіть назву cookie для видалення.", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)
    flash("Запит на видалення cookie виконано.", "success")
    return response


@users_bp.route("/delete-all-cookies", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

    response = make_response(redirect(url_for("users.profile")))

    for key in request.cookies:
        if key not in {"session", "theme"}:
            response.delete_cookie(key)

    flash("Користувацькі cookies видалено.", "success")
    return response


@users_bp.route("/set-theme/<theme>", methods=["POST"])
def set_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

    if theme not in {"light", "dark"}:
        flash("Невідома тема оформлення.", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("theme", theme, max_age=30 * 24 * 60 * 60)
    flash("Тему оформлення змінено.", "success")
    return response
