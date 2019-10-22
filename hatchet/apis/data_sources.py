from flask_restplus import Namespace, Resource

import hatchet.db.meta_models as db
import hatchet.db.crud.base as queries
from hatchet.apis.serializers import data_source
from hatchet.util import default_list_parser


ns = Namespace("dataSources", description="Data-Source related operations")
parser = default_list_parser(namespace=ns)


@ns.route("/")
class DataSourceCollection(Resource):
    @ns.doc('list data sources', parser=parser)
    @ns.marshal_with(data_source)
    def get(self):
        args = parser.parse_args()
        return queries.list_resources(db.DataSource)

    @ns.expect(data_source)
    @ns.doc("create a new data source")
    @ns.marshal_with(data_source)
    def post(self):
        return queries.persist_resource(ns.payload, db.DataSource)


@ns.route("/<int:id>")
@ns.response(404, 'Data Source not found')
@ns.param('id', 'The data-source identifier')
class DataSource(Resource):
    @ns.doc("get data-source by id")
    @ns.marshal_with(data_source)
    def get(self, id: int):
        return queries.get_resource(id, db.DataSource)

    @ns.expect(data_source)
    @ns.doc("update data-source")
    @ns.marshal_with(data_source)
    def put(self, id: int):
        return queries.edit_resource(id, ns.payload, db.DataSource)

    @ns.doc("delete data-source")
    @ns.response(204, "data-source deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.DataSource)
        return ""
