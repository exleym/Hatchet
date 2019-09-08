from flask_restplus import Namespace, Resource, fields

import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.apis.serializers import division

from hatchet.db.crud.divisions import (
    edit_division,
    list_divisions,
    persist_division,
    remove_division_by_id
)

ns = Namespace("divisions", description="division related operations")


@ns.route("/")
class DivisionCollection(Resource):
    @ns.doc('list divisions')
    @ns.marshal_with(division)
    def get(self):
        return queries.list_resources(db.Division)

    @ns.expect(division)
    @ns.doc("create a new division")
    @ns.marshal_with(division)
    def post(self):
        return queries.persist_resource(ns.payload, db.Division)


@ns.route("/<int:id>")
@ns.response(404, 'Division not found')
@ns.param('id', 'The division identifier')
class Division(Resource):
    @ns.doc("get division by id")
    @ns.marshal_with(division)
    def get(self, id: int):
        return queries.get_resource(id, db.Division)

    @ns.expect(division)
    @ns.doc("update division")
    @ns.marshal_with(division)
    def put(self, id: int):
        return queries.edit_resource(id, ns.payload, db.Division)

    @ns.doc("delete division")
    @ns.response(204, "division deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Division)
        return ""
