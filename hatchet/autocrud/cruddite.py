from flask_restplus import Api, Namespace, Resource
from flask_restplus.fields import Nested
import flask_sqlalchemy as db
import logging
from marshmallow import Schema
from typing import List
import hatchet.db.crud.base as queries
from hatchet.extensions import filtr
from hatchet.resources.schemas.converters import MarshmallowRestplusConverter
from hatchet.resources.schemas.schemas import PostFilterSchema, SearchSchema
from hatchet.util import default_list_parser


logger = logging.getLogger(__name__)
search_schema = SearchSchema()


class Cruddite(object):
    def __init__(self, namespace: Namespace, resource: type(db.Model),
                 schema: type(Schema), description: str = None,
                 rp_model = None, parser_args: List[str] = None):
        self.ns = namespace
        self.resource = resource
        self.schema = schema()
        self.converter = MarshmallowRestplusConverter(api=self.ns)
        self.description = description
        self.rp_model = rp_model
        self.parser = default_list_parser(namespace=self.ns)
        parser_args = parser_args or []
        self.converter.create_model(PostFilterSchema)
        self.search_model = self.converter.create_model(SearchSchema)
        for p in parser_args:
            self.parser.add_argument(p)

    def create_collection_endpoints(self):

        @self.ns.route("")
        class ResourceCollection(Resource):

            @self.ns.doc(f"list of {self.ns.name} resources", parser=self.parser)
            @self.ns.marshal_with(self.rp_model, mask=self.default_mask)
            def get(subclass_self):
                args = self.parser.parse_args()
                return queries.list_resources(self.resource, **args)

            @self.ns.expect(self.rp_model, validate=False)
            @self.ns.doc(f"create a {self.ns.name}")
            @self.ns.marshal_with(self.rp_model)
            def post(subclass_self):
                data = self.schema.load(self.ns.payload)
                model = queries.persist_resource(data, self.resource)
                return model, 201

    def create_single_resource_endpoints(self):
        
        @self.ns.route("/<int:id>")
        @self.ns.response(404, "Resource not found")
        @self.ns.param("id", f"The {self.ns.name} identifier")
        class IndividualEntity(Resource):

            @self.ns.doc("get resource by id")
            @self.ns.marshal_with(self.rp_model)
            def get(subclass_self, id: int):
                resource = queries.get_resource(id=id, model=self.resource)
                return resource

            @self.ns.expect(self.rp_model)
            @self.ns.doc("update resource")
            @self.ns.marshal_with(self.rp_model)
            def put(subclass_self, id: int):
                data = self.schema.load(self.ns.payload)
                return queries.edit_resource(id=id, data=data, model=self.resource)

            @self.ns.doc("delete resource")
            @self.ns.response(204, "resource deleted")
            def delete(subclass_self, id: int):
                queries.remove_resource_by_id(id, model=self.resource)
                return "", 204

    def create_search_endpoint(self):

        @self.ns.route("/search")
        class ResourceSearch(Resource):

            @self.ns.doc(f"execute a resource search for {self.ns.name}")
            @self.ns.expect(self.search_model)
            @self.ns.marshal_with(self.rp_model)
            def post(subclass_self):
                filters = self.ns.payload.get("filters")
                return filtr.search(
                    DbModel=self.resource,
                    filters=filters,
                    ModelSchema=self.schema
                )

    @property
    def default_mask(self):
        fields = [k for k, v in self.rp_model.items() if not isinstance(v, Nested)]
        return ",".join(fields)