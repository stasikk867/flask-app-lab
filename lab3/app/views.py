from flask import render_template, request
from . import app


@app.route("/")
def resume():
    return render_template(
        "resume.html",
        title="Резюме"
    )


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    message = None

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        text = request.form.get("message")

        message = f"Дякуємо, {name}! Ваше повідомлення отримано."

    return render_template(
        "contacts.html",
        title="Контакти",
        message=message
    )