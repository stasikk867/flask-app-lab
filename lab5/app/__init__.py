
from flask import Flask
from flask_wtf.csrf import CSRFProtect

from config import Config


csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)

    from app.routes import main_bp
    from app.products import products_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix="/product")

    return app
