import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from app.config import config_by_name
from app.extensions import db, migrate


csrf = CSRFProtect()


def create_app(config_name=None):
    app = Flask(__name__)

    config_name = config_name or os.getenv(
        "FLASK_CONFIG",
        "development"
    )

    app.config.from_object(config_by_name[config_name])

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.routes import main_bp
    from app.products import products_bp
    from app.posts import posts_bp
    from app.posts.models import Post

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix="/product")
    app.register_blueprint(posts_bp, url_prefix="/post")

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app


