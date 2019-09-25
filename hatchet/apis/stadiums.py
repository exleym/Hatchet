from flask_restplus import Namespace, Resource, fields

import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.apis.serializers import stadium


ns = Namespace("stadiums", description="stadium related operations")


@ns.route("/")
class StadiumCollection(Resource):
    @ns.doc('list stadiums')
    @ns.marshal_with(stadium)
    def get(self):
        return queries.list_resources(db.Stadium)

    @ns.expect(stadium)
    @ns.doc("create a new stadium")
    @ns.marshal_with(stadium)
    def post(self):
        return queries.persist_resource(ns.payload, db.Stadium)


@ns.route("/<int:id>")
@ns.response(404, 'Stadium not found')
@ns.param('id', 'The stadium identifier')
class Stadium(Resource):
    @ns.doc("get stadium by id")
    @ns.marshal_with(stadium)
    def get(self, id: int):
        return queries.get_resource(id, db.Stadium)

    @ns.expect(stadium)
    @ns.doc("update stadium")
    @ns.marshal_with(stadium)
    def put(self, id: int):
        return queries.edit_resource(id, ns.payload, db.Stadium)

    @ns.doc("delete stadium")
    @ns.response(204, "stadium deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Stadium)
        return ""
