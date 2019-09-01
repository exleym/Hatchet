from flask import Blueprint
from flask_restplus import Api

from .apis.conferences import api as ns_conferences
from .apis.divisions import api as ns_divisions

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="Hatchet API",
    version="1.0",
    description="API for managing Hatchet CFB data"
)

api.add_namespace(ns_conferences)
api.add_namespace(ns_divisions)
