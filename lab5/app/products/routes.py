
import os
import uuid

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
    abort,
    request,
)
from werkzeug.utils import secure_filename
from tinydb import TinyDB
from tinydb.queries import Query

from . import products_bp
from app.forms import ProductForm


def get_db():
    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "data"
    )
    os.makedirs(data_dir, exist_ok=True)

    return TinyDB(os.path.join(data_dir, "products.json"))


def save_image(file):
    if not file or not file.filename:
        return None

    filename = secure_filename(file.filename)
    extension = filename.rsplit(".", 1)[-1].lower()

    if extension not in current_app.config["ALLOWED_EXTENSIONS"]:
        raise ValueError("Дозволені формати: PNG, JPG, JPEG.")

    unique_filename = f"{uuid.uuid4().hex}.{extension}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    file.save(os.path.join(upload_folder, unique_filename))

    return unique_filename


@products_bp.route("/")
def product_list():
    db = get_db()
    products = db.all()
    db.close()

    return render_template(
        "products/list.html",
        products=products
    )


@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    db = get_db()
    product = db.get(Query().id == product_id)
    db.close()

    if product is None:
        abort(404)

    return render_template(
        "products/detail.html",
        product=product
    )


@products_bp.route("/create", methods=["GET", "POST"])
def product_create():
    form = ProductForm()

    if form.validate_on_submit():
        try:
            image_filename = save_image(form.image.data)
        except ValueError as error:
            flash(str(error), "error")
            return render_template(
                "products/create.html",
                form=form
            )

        db = get_db()
        products = db.all()

        product_id = max(
            (product["id"] for product in products),
            default=0
        ) + 1

        db.insert({
            "id": product_id,
            "name": form.name.data,
            "price": float(form.price.data),
            "description": form.description.data,
            "image": image_filename
        })

        db.close()

        flash("Товар успішно додано!", "success")
        return redirect(url_for("products.product_list"))

    return render_template(
        "products/create.html",
        form=form
    )


@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    db = get_db()
    product = db.get(Query().id == product_id)

    if product is None:
        db.close()
        abort(404)

    form = ProductForm()

    if request.method == "GET":
        form.name.data = product["name"]
        form.price.data = str(product["price"])
        form.description.data = product["description"]

    if form.validate_on_submit():
        try:
            image_filename = save_image(form.image.data)
        except ValueError as error:
            flash(str(error), "error")
            db.close()
            return render_template(
                "products/edit.html",
                form=form,
                product=product
            )

        updated_product = {
            "id": product_id,
            "name": form.name.data,
            "price": float(form.price.data),
            "description": form.description.data,
            "image": image_filename or product.get("image")
        }

        db.update(
            updated_product,
            Query().id == product_id
        )

        db.close()

        flash("Товар успішно оновлено!", "success")
        return redirect(
            url_for("products.product_detail", product_id=product_id)
        )

    db.close()

    return render_template(
        "products/edit.html",
        form=form,
        product=product
    )


@products_bp.route("/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    db = get_db()
    product = db.get(Query().id == product_id)

    if product is None:
        db.close()
        abort(404)

    if product.get("image"):
        image_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            product["image"]
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    db.remove(Query().id == product_id)
    db.close()

    flash("Товар успішно видалено!", "success")
    return redirect(url_for("products.product_list"))



