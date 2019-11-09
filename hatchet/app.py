from flask import Flask, jsonify, redirect
from flask_cors import CORS
import logging
from marshmallow.exceptions import ValidationError


from hatchet import Environment
from hatchet.extensions import db, filtr
from config import Config

from hatchet.apis.api_v1 import blueprint as api_v1
from hatchet.db.seed_data import insert_seed_data
from hatchet.util import error


logger = logging.getLogger(__name__)


def create_app(env='prd') -> Flask:
    """ application factory creates and configures app """
    app = Flask(__name__)
    configure_app(app, env)
    register_extensions(app)
    setup_db(app)
    register_error_handlers(app)
    register_blueprints(app)
    add_special_routes(app)
    return app


def configure_app(app: Flask, env: str) -> None:
    config = Config.get(env)
    app.config.from_object(config)
    app.logger.setLevel(logging.INFO)
    Environment.set(config.ENV)


def register_blueprints(app: Flask):
    app.register_blueprint(api_v1, url_prefix="/api/v1")


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    filtr.init_app(app)
    CORS(app)


def setup_db(app: Flask) -> None:
    if app.config.get('CREATE_SCHEMA'):
        with app.app_context():
            db.create_all()
            if app.config.get("SEED_DATA"):
                insert_seed_data()



def add_special_routes(app: Flask):
    @app.route("/swagger")
    def swagger():
        return redirect("/api/v1")


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(ValidationError)
    def validation_error_handler(err):
        logger.error("marshmallow validation error", err)
        return error(422, [{"message": "Validation error", "details": str(err)}])

    @app.errorhandler(Exception)
    def generic_error_handler(err):
        logger.error("unhandled application exception", err)
        code = getattr(err, "status_code", 500)
        message = getattr(err, "messages", "uncaught exception")
        return error(code, [dict(message=message, details=str(err))])
