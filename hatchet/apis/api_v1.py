from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="Hatchet API",
    version="1.0",
    description="API for managing Hatchet CFB data"
)

from hatchet.apis.conferences import ns as ns_conferences
from hatchet.apis.divisions import ns as ns_divisions

api.add_namespace(ns_conferences)
api.add_namespace(ns_divisions)
