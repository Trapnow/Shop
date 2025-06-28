from flask import Flask

from .config import Config
from .extensions import db, migrate, login_manager
from .routes.list_books import book
from .routes.user import user
from .routes.cart import cart
from .routes.order import order

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(book)
    app.register_blueprint(user)
    app.register_blueprint(cart)
    app.register_blueprint(order)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "user.login"
    login_manager.login_message = "Сначала войдите в свой аккаунт"

    with app.app_context():
        db.create_all()

    return app
