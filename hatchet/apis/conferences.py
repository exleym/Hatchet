from flask_restplus import Namespace, Resource, fields

import hatchet.db.models as db
import hatchet.db.crud.base as queries


api = Namespace("conferences", description="conference related operations")


conference = api.model("Conference", {
    "id": fields.Integer(),
    "code": fields.String(),
    "name": fields.String(),
    "shortName": fields.String(),
    "inceptionYear": fields.Integer(attribute="inception_year")
})


@api.route("/")
class ConferenceCollection(Resource):
    @api.doc('list conferences')
    @api.marshal_with(conference)
    def get(self):
        return queries.list_resources(db.Conference)

    @api.expect(conference)
    @api.doc("create a new conference")
    @api.marshal_with(conference)
    def post(self):
        return queries.persist_resource(api.payload, db.Conference)


@api.route("/<int:id>")
@api.response(404, 'Conference not found')
@api.param('id', 'The conference identifier')
class Conference(Resource):
    @api.doc("get conference by id")
    @api.marshal_with(conference)
    def get(self, id: int):
        return queries.get_resource(id, db.Conference)

    @api.expect(conference)
    @api.doc("update conference")
    @api.marshal_with(conference)
    def put(self, id: int):
        return queries.edit_resource(id, api.payload, db.Conference)

    @api.doc("delete conference")
    @api.response(204, "conference deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Conference)
        return ""
