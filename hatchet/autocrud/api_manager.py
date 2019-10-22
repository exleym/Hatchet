from flask import Blueprint
from flask_restplus import Api, Namespace
from flask_sqlalchemy import Model
from marshmallow import Schema
from hatchet.autocrud.cruddite import Cruddite
from hatchet.resources.schemas.converters import MarshmallowRestplusConverter
from hatchet.util import default_list_parser


class APIManager(object):

    def __name__(self, title: str, version: str, description: str = None):
        self.blueprint = Blueprint("api", __name__)
        self.resources = {}
        self.api = Api(
            self.blueprint,
            title=title,
            version=version,
            description=description
        )
        self.schema_converter = MarshmallowRestplusConverter(api=self.api)

    def add_resource(self, name: str, resource: type(Model),
                     schema: type(Schema), description: str = None):
        ns = Namespace(name=name, description=description)
        rp_model = self.schema_converter.create_model(schema=schema)
        parser = default_list_parser(namespace=ns)
        self.add_collection_endpoints(
            ns=ns,
            resource=resource,
            schema=schema,
            rp_model=rp_model
        )
        self.api.add_namespace(ns)

    def add_collection_endpoints(self, ns: Namespace, resource: type(Model),
                                 schema: type(Schema), rp_model,
                                 description: str = None):
        cruddite = Cruddite(api=self.api, name=ns.name)


