from flask_restplus import Namespace, Resource, fields

from hatchet.db.crud.conferences import (
    edit_conference,
    list_conferences,
    persist_conference,
    remove_conference_by_id
)

api = Namespace("conferences", description="conference related operations")


conference = api.model("Conference", {
    "id": fields.Integer(),
    "code": fields.String(),
    "name": fields.String(),
    "shortName": fields.String(),
    "inceptionYear": fields.Integer(attribute="inception_year")
})


class Conferences(Resource):
    @api.marshal_with(conference)
    def get(self):
        return list_conferences()

    @api.marshal_with(conference)
    def post(self):