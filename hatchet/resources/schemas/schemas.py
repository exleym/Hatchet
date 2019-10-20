from marshmallow import fields

from hatchet.resources.schemas.validators import (
    modern_datetime_validator, modern_year_validator, score_validator
)
from hatchet.resources.schemas.base import BaseSchema



class SubdivisionSchema(BaseSchema):
    code = fields.String()
    name = fields.String()
    division = fields.Integer()



class ConferenceSchema(BaseSchema):
    code = fields.String()
    name = fields.String()
    shortName = fields.String(attribute="short_name")
    subdivisionId = fields.Integer(attribute="subdivision_id")
    inceptionYear = fields.String(
        attribute="inception_year",
        validate=modern_year_validator,
        allow_none=True
    )
    subdivision =fields.Nested("Subdivision")


class DivisionSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    conferenceId = fields.Integer(attribute="conference_id")
    name = fields.String(attribute="name", dump_only=True)


class StadiumSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    nickname = fields.String()
    built = fields.Integer()
    capacity = fields.Integer()
    surface = fields.String()


class TeamSchema(BaseSchema):
    id = fields.Integer()
    code = fields.String()
    name = fields.String()
    shortName = fields.String(attribute='short_name', allow_none=True)
    mascot = fields.String()
    conferenceId = fields.Integer(attribute='conference_id', load_only=True)
    divisionId = fields.Integer(attribute='division_id')
    stadiumId = fields.Integer(attribute='stadium_id', allow_none=True)


class GameParticipantSchema(BaseSchema):
    id = fields.Integer()
    teamId = fields.Integer(attribute='team_id')
    gameId = fields.Integer(attribute='game_id')
    locationTypeId = fields.Integer(attribute='location_type_id')
    score = fields.Integer(validate=score_validator, allow_none=True)
    team = fields.Nested('TeamSchema', many=False)


class GameSchema(BaseSchema):
    id = fields.Integer()
    kickoffTime = fields.DateTime(
        attribute='game_time',
        validate=modern_datetime_validator
    )
    stadiumId = fields.Int(attribute='stadium_id', allow_none=True)
    espnId = fields.Int(attribute='espn_id', allow_none=True)
    participants = fields.Nested('GameParticipantSchema', many=True)
    winner = fields.Nested("GameParticipantSchema", many=False)


class ScoreSchema(BaseSchema):
    teamId = fields.Integer(attribute="team_id")
    score = fields.Integer()


class ErrorSchema(BaseSchema):
    code = fields.String()
    name = fields.String()
