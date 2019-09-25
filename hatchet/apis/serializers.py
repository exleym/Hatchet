from flask_restplus import fields
from hatchet.apis.api_v1 import api


conference = api.model("Conference", {
    "id": fields.Integer(dump_only=True),
    "code": fields.String(),
    "name": fields.String(),
    "shortName": fields.String(),
    "inceptionYear": fields.Integer(attribute="inception_year")
})


division = api.model("Division", {
    "id": fields.Integer(dump_only=True),
    "conferenceId": fields.Integer(attribute="conference_id"),
    "name": fields.String(),
    # "conference": fields.Nested("conference")
})


team = api.model("Team", {
    "id": fields.Integer(dump_only=True),
    "name": fields.String(),
    "shortName": fields.String(attribute='short_name', allow_none=True),
    "mascot": fields.String(),
    "conferenceId": fields.Integer(attribute='conference_id', load_only=True),
    "divisionId": fields.Integer(attribute='division_id'),
    "stadiumId": fields.Integer(attribute='stadium_id', allow_none=True)
})
