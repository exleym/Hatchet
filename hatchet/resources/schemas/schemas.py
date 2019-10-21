from marshmallow import fields

from hatchet.resources.schemas.validators import (
    modern_datetime_validator, modern_year_validator, score_validator
)
from hatchet.resources.schemas.base import BaseSchema



class CoachSchema(BaseSchema):
    firstName = fields.String(attribute="first_name")
    lastName = fields.String(attribute="last_name")
    dateOfBirth = fields.Date(attribute="dob")


class ConferenceSchema(BaseSchema):
    subdivisionId = fields.Integer(attribute="subdivision_id")
    code = fields.String()
    name = fields.String()
    shortName = fields.String(attribute="short_name")
    inceptionYear = fields.String(
        attribute="inception_year",
        validate=modern_year_validator,
        allow_none=True
    )
    subdivision =fields.Nested("SubdivisionSchema")


class DivisionSchema(BaseSchema):
    conferenceId = fields.Integer(attribute="conference_id")
    name = fields.String(attribute="name", dump_only=True)
    conference = fields.Nested("ConferenceSchema", allow_none=True)


class ErrorSchema(BaseSchema):
    code = fields.String()
    name = fields.String()


class GameParticipantSchema(BaseSchema):
    teamId = fields.Integer(attribute='team_id')
    gameId = fields.Integer(attribute='game_id')
    locationTypeId = fields.Integer(attribute='location_type_id')
    score = fields.Integer(validate=score_validator, allow_none=True)
    team = fields.Nested('TeamSchema', many=False)


class GameSchema(BaseSchema):
    kickoffTime = fields.DateTime(
        attribute='game_time',
        validate=modern_datetime_validator
    )
    stadiumId = fields.Integer(attribute='stadium_id', allow_none=True)
    espnId = fields.Integer(attribute='espn_id', allow_none=True)
    participants = fields.List(fields.Nested('GameParticipantSchema'))
    winner = fields.Nested(
        "GameParticipantSchema",
        many=False,
        allow_none=True,
        dump_only=True
    )


class PlayerSchema(BaseSchema):
    firstName = fields.String(attribute="first_name")
    lastName = fields.String(attribute="last_name")
    dateOfBirth = fields.Date(attribute="dob")


class ScoreSchema(BaseSchema):
    teamId = fields.Integer(attribute="team_id")
    score = fields.Integer()


class StadiumSchema(BaseSchema):
    code = fields.String()
    name = fields.String()
    state = fields.String()
    city = fields.String()
    latitude = fields.String()
    longitude = fields.String()
    built = fields.Integer()
    capacity = fields.Integer()
    surfaceId = fields.Integer(attribute="surface_id")
    surface = fields.Nested("SurfaceSchema")


class SubdivisionSchema(BaseSchema):
    code = fields.String(example="FBS")
    name = fields.String(example="Football Bowl Subdivision")
    division = fields.Integer(example=1)


class SurfaceSchema(BaseSchema):
    code = fields.String()
    name = fields.String()
    category = fields.String()


class TeamSchema(BaseSchema):
    code = fields.String()
    name = fields.String()
    shortName = fields.String(attribute='short_name', allow_none=True)
    mascot = fields.String()
    conferenceId = fields.Integer(attribute='conference_id', load_only=True)
    divisionId = fields.Integer(attribute='division_id')
    stadiumId = fields.Integer(attribute='stadium_id', allow_none=True)
    stadium = fields.Nested("StadiumSchema", dump_only=True)
    conference = fields.Nested("ConferenceSchema", dump_only=True)
    division = fields.Nested("DivisionSchema", dump_only=True)
