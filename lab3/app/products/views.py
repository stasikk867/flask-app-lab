from flask import render_template, abort
from . import products_bp


products = [
    {
        "id": 1,
        "name": "Ноутбук",
        "price": 35000,
        "description": "Потужний ноутбук для навчання та роботи."
    },
    {
        "id": 2,
        "name": "Смартфон",
        "price": 25000,
        "description": "Сучасний смартфон із якісною камерою."
    },
    {
        "id": 3,
        "name": "Навушники",
        "price": 5000,
        "description": "Бездротові навушники для музики та дзвінків."
    }
]


@products_bp.route("/")
def product_list():
    return render_template(
        "products/list.html",
        products=products
    )


@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = next(
        (item for item in products if item["id"] == product_id),
        None
    )

    if product is None:
        abort(404)

    return render_template(
        "products/detail.html",
        product=product
    )