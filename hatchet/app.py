from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint


from hatchet.api import api
from hatchet.errors import *
from hatchet.extensions import cors, db

from config import Config


error_schema = ErrorSchema()


def create_app(env='prd') -> Flask:
    """ application factory creates and configures app """
    app = Flask(__name__)
    configure_app(app, env)
    register_extensions(app)
    register_blueprints(app)
    return app


def configure_app(app: Flask, env: str) -> None:
    config = Config.get(env)
    app.config.from_object(config)


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    cors.init_app(app)


def register_blueprints(app: Flask) -> None:
    SWAGGER_URL_PREFIX = '/api/v1/swagger'
    app.register_blueprint(api, url_prefix='/api/v1')
    app.register_blueprint(get_swaggerui_blueprint(SWAGGER_URL_PREFIX,
                                                   '/static/swagger.yml'),
                           url_prefix=SWAGGER_URL_PREFIX)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(MissingResourceException)
    def missing_resource(err):
        return error_schema.dump(err), err.status_code