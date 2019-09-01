from flask_restplus import Namespace, Resource, fields

from hatchet.db.crud.divisions import (
    edit_division,
    list_divisions,
    persist_division,
    remove_division_by_id
)

api = Namespace("divisions", description="division related operations")


division = api.model("Division", {
    "id": fields.Integer(),
    "conferenceId": fields.Integer(attribute="conference_id"),
    "name": fields.String(),
    # "conference": fields.Nested("conference")
})


@api.route("/")
class DivisionCollection(Resource):
    @api.doc('list divisions')
    @api.marshal_with(division)
    def get(self):
        return list_divisions()

    @api.expect(division)
    @api.doc("create a new division")
    @api.marshal_with(division)
    def post(self):
        return persist_division(api.payload)


@api.route("/<int:id>")
@api.response(404, 'Division not found')
@api.param('id', 'The division identifier')
class Division(Resource):
    @api.doc("get division by id")
    @api.marshal_with(division)
    def get(self, id: int):
        return list_divisions(division_id=id)

    @api.expect(division)
    @api.doc("update division")
    @api.marshal_with(division)
    def put(self, id: int):
        return edit_division(division_id=id, data=api.payload)

    @api.doc("delete division")
    @api.response(204, "division deleted")
    def delete(self, id: int):
        remove_division_by_id(id)
        return ""
