from flask import Flask, jsonify, redirect
from flask_cors import CORS
import logging


from hatchet import Environment
from hatchet.extensions import db
from config import Config

from hatchet.apis.api_v1 import blueprint as api_v1
from hatchet.db.seed_data import insert_seed_data


def create_app(env='prd') -> Flask:
    """ application factory creates and configures app """
    app = Flask(__name__)
    configure_app(app, env)
    register_extensions(app)
    register_error_handlers(app)

    @app.errorhandler(Exception)
    def handle(exception):
        raise exception

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
    CORS(app)
    if app.config.get('CREATE_SCHEMA'):
        with app.app_context():
            db.create_all()
            insert_seed_data()


def add_special_routes(app: Flask):
    @app.route("/swagger")
    def swagger():
        return redirect("/api/v1")


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(Exception)
    def generic_error_handler(err):
        return jsonify({"errors": [{'message': 'uncaught exception',
                                    'err': str(err)}]}), 500
