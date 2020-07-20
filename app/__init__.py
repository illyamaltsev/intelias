import logging
import sys

from flask import Flask

from app.payment import models
from app.payment.views import payment_bp


def register_blueprints(app):
    app.register_blueprint(payment_bp)


def setup_logger(app):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)


def setup_db(app):
    db = models.db
    db.init_app(app)


def create_app(config_object=None):
    app = Flask(__name__)

    app.config.from_object(config_object)

    setup_logger(app)

    setup_db(app)

    register_blueprints(app)

    return app
