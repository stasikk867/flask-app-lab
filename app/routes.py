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

data_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data"
)

os.makedirs(data_dir, exist_ok=True)

log_file = os.path.join(data_dir, "contact.log")

logger = logging.getLogger("contact_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    try:
        handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(message)s")
        )
        logger.addHandler(handler)
    except OSError:
        pass


@main_bp.route("/", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        message = (
            f"Ім'я: {form.name.data} | "
            f"Email: {form.email.data} | "
            f"Телефон: {form.phone.data} | "
            f"Тема: {form.subject.data} | "
            f"Повідомлення: {form.message.data}"
        )

        try:
            with open(log_file, "a", encoding="utf-8") as file:
                file.write(message + "\n")

            logger.info("Нове повідомлення: %s", message)

            flash(
                "Повідомлення успішно надіслано та записано!",
                "success"
            )

        except OSError:
            flash(
                "Не вдалося зберегти повідомлення. Спробуйте ще раз.",
                "error"
            )

        return redirect(url_for("main.contact"))

    if form.is_submitted():
        flash(
            "Не вдалося надіслати повідомлення. Перевірте правильність заповнення форми.",
            "error"
        )

    return render_template("contact.html", form=form)