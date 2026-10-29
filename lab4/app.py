
from datetime import timedelta

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    make_response,
)

app = Flask(__name__)
app.secret_key = "lab4_secret_key_2026"


# Головна сторінка
@app.route("/")
def home():
    return redirect(url_for("login"))


# Вхід у систему
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Тестові облікові дані без бази даних
        if username == "user1" and password == "12345":
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("profile"))

        flash("Неправильний логін або пароль!", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


# Профіль користувача
@app.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("login"))

    cookies = dict(request.cookies)
    theme = request.cookies.get("theme", "light")

    return render_template(
        "profile.html",
        username=session["username"],
        cookies=cookies,
        theme=theme,
    )


# Вихід із системи
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    response = make_response(redirect(url_for("login")))
    response.delete_cookie(app.config["SESSION_COOKIE_NAME"])
    flash("Ви вийшли із системи.", "info")
    return response


# Додавання cookie
@app.route("/add-cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    days_text = request.form.get("days", "7")

    if not key:
        flash("Введіть ключ cookie!", "error")
        return redirect(url_for("profile"))

    # Не дозволяємо змінювати службові cookies застосунку
    if key in {
        app.config["SESSION_COOKIE_NAME"],
        "theme",
    }:
        flash("Цей ключ зарезервований для застосунку.", "error")
        return redirect(url_for("profile"))

    try:
        days = int(days_text)
        if days < 1:
            raise ValueError
    except (ValueError, TypeError):
        flash("Термін дії має бути цілим числом від 1 дня!", "error")
        return redirect(url_for("profile"))

    response = make_response(redirect(url_for("profile")))
    response.set_cookie(
        key,
        value,
        max_age=int(timedelta(days=days).total_seconds()),
        httponly=True,
        samesite="Lax",
    )

    flash(f"Cookie «{key}» успішно додано!", "success")
    return response


# Видалення cookie за ключем
@app.route("/delete-cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("login"))

    key = request.form.get("key", "").strip()

    if not key:
        flash("Введіть ключ cookie для видалення!", "error")
        return redirect(url_for("profile"))

    if key in {
        app.config["SESSION_COOKIE_NAME"],
        "theme",
    }:
        flash("Цей cookie не можна видалити цим способом.", "error")
        return redirect(url_for("profile"))

    response = make_response(redirect(url_for("profile")))

    if key in request.cookies:
        response.delete_cookie(key)
        flash(f"Cookie «{key}» видалено.", "success")
    else:
        flash(f"Cookie «{key}» не знайдено.", "error")

    return response


# Видалення всіх користувацьких cookies
@app.route("/delete-all-cookies", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("login"))

    response = make_response(redirect(url_for("profile")))

    # Залишаємо cookie сесії, щоб користувач не вийшов із профілю.
    # Решта cookies, зокрема тема, видаляються.
    for key in request.cookies:
        if key != app.config["SESSION_COOKIE_NAME"]:
            response.delete_cookie(key)

    flash("Усі користувацькі cookies видалено.", "success")
    return response


# Зміна колірної схеми
@app.route("/set-theme/<theme>", methods=["POST"])
def set_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("login"))

    if theme not in ("light", "dark"):
        flash("Невідома колірна схема!", "error")
        return redirect(url_for("profile"))

    response = make_response(redirect(url_for("profile")))
    response.set_cookie(
        "theme",
        theme,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="Lax",
    )

    flash("Колірну схему змінено!", "success")
    return response


if __name__ == "__main__":
    app.run(debug=True)
