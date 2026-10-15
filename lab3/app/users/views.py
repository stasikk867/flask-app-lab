from flask import render_template, request, redirect, url_for
from . import users_bp


@users_bp.route("/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template(
        "users/hi.html",
        name=name,
        age=age
    )


@users_bp.route("/admin")
def admin():
    to_url = url_for(
        "users.greetings",
        name="administrator",
        age=45,
        _external=True
    )

    return redirect(to_url)