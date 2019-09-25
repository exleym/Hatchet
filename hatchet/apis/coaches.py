from flask_restplus import Namespace, Resource, fields

import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.apis.serializers import coach, team
from hatchet.util import default_list_parser



ns = Namespace("coaches", description="coach related operations")
parser = default_list_parser(namespace=ns)


@ns.route("/")
class CoachCollection(Resource):
    @ns.doc('list coaches', parser=parser)
    @ns.marshal_with(coach)
    def get(self):
        args = parser.parse_args()
        return queries.list_resources(db.Coach)

    @ns.expect(coach)
    @ns.doc("create a new coach")
    @ns.marshal_with(coach)
    def post(self):
        return queries.persist_resource(ns.payload, db.Coach)


@ns.route("/<int:id>")
@ns.response(404, 'Coach not found')
@ns.param('id', 'The coach identifier')
class Coach(Resource):
    @ns.doc("get coach by id")
    @ns.marshal_with(coach)
    def get(self, id: int):
        return queries.get_resource(id, db.Coach)

    @ns.expect(coach)
    @ns.doc("update coach")
    @ns.marshal_with(coach)
    def put(self, id: int):
        return queries.edit_resource(id, ns.payload, db.Coach)

    @ns.doc("delete coach")
    @ns.response(204, "coach deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Coach)
        return ""
