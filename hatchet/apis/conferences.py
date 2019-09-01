from flask_restplus import Namespace, Resource, fields
import hatchet.db.crud.core as queries
import hatchet.db.models as db


api = Namespace("conferences", description="conference related operations")


conference = api.model("Conference", {
    "id": fields.Integer(),
    "code": fields.String(),
    "name": fields.String(),
    "shortName": fields.String(),
    "inceptionYear": fields.Integer(attribute="inception_year")
})


@api.route("/conferences")
class ConferenceCollection(Resource):
    @api.doc("list conferences")
    @api.marshal_with(conference)
    def get(self):
        return queries.list_resources(db.Conference)

    @api.doc("create conference")
    @api.expect(conference)
    @api.marshal_with(conference)
    def post(self):
        return queries.create_resource(api.payload, db.Conference)


@api.route("/conferences/<int:id>")
class Conferences(Resource):

    @api.doc("get conference by id")
    @api.marshal_with(conference)
    def get(self, id: int):
        return queries.get_resource(id=id, model=db.Conference)

    @api.doc("update conference")
    @api.expect(conference)
    @api.marshal_with(conference)
    def put(self, id: int):
        return queries.update_resource(id=id, data=api.payload, model=db.Conference)


    @api.doc("delete conference")
    def delete(self, id: int):
        return queries.remove_resource(id=id, model=db.Conference)