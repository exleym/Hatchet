from flask_restplus import Namespace, Resource, fields

import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.apis.serializers import team


ns = Namespace("teams", description="team related operations")


@ns.route("/")
class TeamCollection(Resource):
    @ns.doc('list teams')
    @ns.marshal_with(team)
    def get(self):
        return queries.list_resources(db.Team)

    @ns.expect(team)
    @ns.doc("create a new team")
    @ns.marshal_with(team)
    def post(self):
        return queries.persist_resource(ns.payload, db.Team)


@ns.route("/<int:id>")
@ns.response(404, 'Team not found')
@ns.param('id', 'The team identifier')
class Team(Resource):
    @ns.doc("get team by id")
    @ns.marshal_with(team)
    def get(self, id: int):
        return queries.get_resource(id, db.Team)

    @ns.expect(team)
    @ns.doc("update team")
    @ns.marshal_with(team)
    def put(self, id: int):
        return queries.edit_resource(id, ns.payload, db.Team)

    @ns.doc("delete team")
    @ns.response(204, "team deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Team)
        return ""


# @ns.route("/<int:id>/teams")
# @ns.param("id", "the team identifier")
# class TeamTeams(Resource):
#     @ns.doc("get team teams")
#     @ns.marshal_with(team)
#     def get(self, id: int):
#         conf = queries.get_resource(id, db.Team)
#         return conf.members