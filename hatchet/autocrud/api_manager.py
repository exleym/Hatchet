from flask import Blueprint
from flask_restplus import Api, Namespace
from flask_sqlalchemy import Model
from marshmallow import Schema
from typing import List
from hatchet.autocrud.cruddite import Cruddite
from hatchet.resources.schemas.converters import MarshmallowRestplusConverter


class APIManager(object):

    def __init__(self, title: str, version: str, description: str = None, api: Api = None):
        # self.blueprint = Blueprint("api", __name__)
        self.resources = {}
        self.serializers = {}
        self.api = api # or Api(
        #     self.blueprint,
        #     title=title,
        #     version=version,
        #     description=description
        # )
        self.schema_converter = MarshmallowRestplusConverter(api=self.api)

    def add_resource(self, name: str, resource: type(Model),
                     schema: type(Schema), description: str = None,
                     parser_args: List[str] = None, include_search: bool = True):
        ns = Namespace(name=name, description=description)
        rp_model = self.get_or_create_model(schema=schema)
        self.add_default_endpoints(
            ns=ns,
            resource=resource,
            schema=schema,
            rp_model=rp_model,
            parser_args=parser_args,
            include_search=include_search
        )
        self.api.add_namespace(ns)
        return ns

    def model(self, name: str):
        return self.schema_converter.get(schema_name=name)

    def create_model(self, schema: type(Schema)):
        return self.schema_converter.create_model(schema=schema)

    def get_or_create_model(self, schema: type(Schema)):
        name = schema.__name__.replace("Schema", "")
        rp_model = self.model(name=name)
        if not rp_model:
            rp_model = self.create_model(schema=schema)
        return rp_model

    def add_default_endpoints(self, ns: Namespace, resource: type(Model),
                              schema: type(Schema), rp_model,
                              description: str = None,
                              parser_args: List[str] = None,
                              include_search: bool = True):
        cruddite = Cruddite(namespace=ns, resource=resource, schema=schema,
                            description=description, rp_model=rp_model,
                            parser_args=parser_args)
        cruddite.create_collection_endpoints()
        cruddite.create_single_resource_endpoints()
        if include_search:
            cruddite.create_search_endpoint()

