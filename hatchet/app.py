from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from marshmallow import ValidationError


from hatchet import Environment
from hatchet.api import api
from hatchet.errors import *
from hatchet.extensions import cors, db, ma
from hatchet.db.crud.location_types import populate_locations

from config import Config


error_schema = ErrorSchema()


def create_app(env='prd') -> Flask:
    """ application factory creates and configures app """
    app = Flask(__name__)
    configure_app(app, env)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    return app


def configure_app(app: Flask, env: str) -> None:
    config = Config.get(env)
    app.config.from_object(config)
    Environment.set(config.ENV)


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    cors.init_app(app)
    ma.init_app(app)
    if app.config.get('CREATE_SCHEMA'):
        with app.app_context():
            db.create_all()
            populate_locations()


def register_blueprints(app: Flask) -> None:
    SWAGGER_URL_PREFIX = '/api/v1/swagger'
    app.register_blueprint(api, url_prefix='/api/v1')
    app.register_blueprint(get_swaggerui_blueprint(SWAGGER_URL_PREFIX,
                                                   '/static/swagger.yml'),
                           url_prefix=SWAGGER_URL_PREFIX)


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(MissingResourceException)
    def missing_resource(err):
        return jsonify(error_schema.dump(err)), err.status_code

    @app.errorhandler(ValidationError)
    def general_exception(err):
        app.logger.error(f"validation error: {err}")
        return jsonify(err.messages), 422

    @app.errorhandler(404)
    def missing_route(error):
        return jsonify({'message': 'missing route', 'url': request.url}), 404

    # @app.errorhandler(Exception)
    # def generic_error_handler(err):
    #     return jsonify({"errors": [{'message': 'uncaught exception',
    #                                 'err': str(err)}]}), 500
