from flask_restplus import Namespace, Resource, fields

import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.apis.serializers import conference, team




@ns.route("/")
class ConferenceCollection(Resource):
    @ns.doc('list conferences')
    @ns.marshal_with(conference)
    def get(self):
        return queries.list_resources(db.Conference)

    @ns.expect(conference)
    @ns.doc("create a new conference")
    @ns.marshal_with(conference)
    def post(self):
        return queries.persist_resource(ns.payload, db.Conference)


@ns.route("/<int:id>")
@ns.response(404, 'Conference not found')
@ns.param('id', 'The conference identifier')
class Conference(Resource):
    @ns.doc("get conference by id")
    @ns.marshal_with(conference)
    def get(self, id: int):
        return queries.get_resource(id, db.Conference)

    @ns.expect(conference)
    @ns.doc("update conference")
    @ns.marshal_with(conference)
    def put(self, id: int):
        return queries.edit_resource(id, ns.payload, db.Conference)

    @ns.doc("delete conference")
    @ns.response(204, "conference deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Conference)
        return ""


@ns.route("/<int:id>/teams")
@ns.param("id", "the conference identifier")
class ConferenceTeams(Resource):
    @ns.doc("get conference teams")
    @ns.marshal_with(team)
    def get(self, id: int):
        conf = queries.get_resource(id, db.Conference)
        return conf.members