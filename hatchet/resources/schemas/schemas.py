from hatchet.resources.schemas.validators import (
    modern_datetime_validator, modern_year_validator, score_validator
)
from marshmallow import fields, Schema


class ConferenceSchema(Schema):
    id = fields.Integer(dump_only=True, allow_none=False)
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


class DivisionSchema(Schema):
    id = fields.Integer(dump_only=True)
    conferenceId = fields.Integer(attribute="conference_id")
    name = fields.String(attribute="name", dump_only=True)


class StadiumSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    nickname = fields.String()
    built = fields.Integer()
    capacity = fields.Integer()
    surface = fields.String()


class TeamSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    shortName = fields.String(attribute='short_name', allow_none=True)
    mascot = fields.String()
    conferenceId = fields.Integer(attribute='conference_id', load_only=True)
    divisionId = fields.Integer(attribute='division_id')
    stadiumId = fields.Integer(attribute='stadium_id', allow_none=True)


class GameParticipantSchema(Schema):
    id = fields.Integer(dump_only=True)
    teamId = fields.Integer(attribute='team_id')
    gameId = fields.Integer(attribute='game_id')
    locationTypeId = fields.Integer(attribute='location_type_id')
    score = fields.Integer(nullable=True, validate=score_validator)
    team = fields.Nested('TeamSchema', many=False)


class GameSchema(Schema):
    id = fields.Integer(dump_only=True)
    kickoffTime = fields.DateTime(attribute='game_time',
                              validate=modern_datetime_validator)
    stadiumId = fields.Int(attribute='stadium_id')
    espnId = fields.Int(attribute='espn_id')
    participants = fields.Nested('GameParticipantSchema', many=True)


class ScoreSchema(Schema):
    teamId = fields.Integer(attribute="team_id")
    score = fields.Integer()


class ErrorSchema(Schema):
    code = fields.String()
    name = fields.String()
