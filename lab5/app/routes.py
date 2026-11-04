
import logging
import os

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)

from app.forms import ContactForm


main_bp = Blueprint("main", __name__)


# Створення папки для збереження повідомлень
data_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data"
)

os.makedirs(data_dir, exist_ok=True)

log_file = os.path.join(data_dir, "contact.log")


# Налаштування журналювання повідомлень
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)


@main_bp.route("/", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        logging.info(
            "Нове повідомлення: Ім'я: %s | Email: %s | Телефон: %s | "
            "Тема: %s | Повідомлення: %s",
            form.name.data,
            form.email.data,
            form.phone.data,
            form.subject.data,
            form.message.data
        )

        flash("Повідомлення успішно надіслано!", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", form=form)
