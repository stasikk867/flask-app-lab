import os
import uuid
from datetime import datetime
from decimal import Decimal

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
    abort,
)
from werkzeug.utils import secure_filename
from tinydb import TinyDB
from tinydb.queries import Query

from . import products_bp
from app.products.forms import ProductForm


def get_db():
    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "data"
    )
    os.makedirs(data_dir, exist_ok=True)

    return TinyDB(os.path.join(data_dir, "products.json"))


def get_products_table(db):
    return db.table("products")


def save_image(file):
    if not file or not file.filename:
        return None

    original_name = secure_filename(file.filename)

    if "." not in original_name:
        raise ValueError("Файл повинен мати розширення PNG, JPG або JPEG.")

    extension = original_name.rsplit(".", 1)[1].lower()

    if extension not in current_app.config["ALLOWED_EXTENSIONS"]:
        raise ValueError("Дозволені формати: PNG, JPG, JPEG.")

    unique_filename = f"{uuid.uuid4().hex}.{extension}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    file.save(os.path.join(upload_folder, unique_filename))

    return unique_filename


def remove_image(filename):
    if not filename:
        return

    image_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    if os.path.isfile(image_path):
        os.remove(image_path)


def get_next_id(products):
    return max(
        (product.get("id", 0) for product in products),
        default=0
    ) + 1


@products_bp.route("/")
def product_list():
    db = get_db()

    try:
        products = get_products_table(db).all()
    finally:
        db.close()

    return render_template(
        "products/list.html",
        products=products
    )


@products_bp.route("/add", methods=["GET", "POST"])
def product_create():
    form = ProductForm()

    if form.validate_on_submit():
        try:
            image_filename = save_image(form.image.data)
        except ValueError as error:
            flash(str(error), "error")
            return render_template("products/create.html", form=form)

        db = get_db()

        try:
            table = get_products_table(db)
            products = table.all()

            product = {
                "id": get_next_id(products),
                "name": form.name.data,
                "content": form.content.data,
                "price": float(Decimal(form.price.data)),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_filename,
                "created_at": datetime.now().isoformat(timespec="seconds")
            }

            table.insert(product)
        finally:
            db.close()

        flash("Товар успішно додано!", "success")
        return redirect(url_for("products.product_list"))

    return render_template(
        "products/create.html",
        form=form
    )


@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    db = get_db()

    try:
        product = get_products_table(db).get(
            Query().id == product_id
        )
    finally:
        db.close()

    if product is None:
        abort(404)

    return render_template(
        "products/detail.html",
        product=product
    )


@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    db = get_db()

    try:
        table = get_products_table(db)
        product = table.get(Query().id == product_id)

        if product is None:
            abort(404)

        form = ProductForm()

        if form.validate_on_submit():
            try:
                image_filename = save_image(form.image.data)
            except ValueError as error:
                flash(str(error), "error")
                return render_template(
                    "products/edit.html",
                    form=form,
                    product=product
                )

            updated_product = {
                "id": product["id"],
                "name": form.name.data,
                "content": form.content.data,
                "price": float(Decimal(form.price.data)),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_filename or product.get("image"),
                "created_at": product["created_at"]
            }

            table.update(
                updated_product,
                Query().id == product_id
            )

            if image_filename and product.get("image"):
                remove_image(product["image"])

            flash("Товар успішно оновлено!", "success")
            return redirect(
                url_for(
                    "products.product_detail",
                    product_id=product_id
                )
            )

        if form.name.data is None:
            form.name.data = product["name"]
            form.content.data = product["content"]
            form.price.data = str(product["price"])
            form.category.data = product["category"]
            form.quantity.data = product["quantity"]

        return render_template(
            "products/edit.html",
            form=form,
            product=product
        )
    finally:
        db.close()


@products_bp.route("/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    db = get_db()

    try:
        table = get_products_table(db)
        product = table.get(Query().id == product_id)

        if product is None:
            abort(404)

        table.remove(Query().id == product_id)

        remove_image(product.get("image"))
    finally:
        db.close()

    flash("Товар успішно видалено!", "success")
    return redirect(url_for("products.product_list"))
