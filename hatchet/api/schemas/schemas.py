from hatchet.extensions import ma, swag
from hatchet.api.schemas.validators import (
    modern_datetime_validator, modern_year_validator, score_validator
)
from marshmallow import fields, Schema


@swag.schema
class ConferenceSchema(Schema):
    id = fields.Integer(dump_only=True, allow_none=False)
    code = fields.String()
    name = fields.String()
    shortName = fields.String(attribute="short_name")
    inceptionYear = fields.String(
        attribute="inception_year",
        validate=modern_year_validator,
        allow_none=True
    )


@swag.schema
class DivisionSchema(Schema):
    id = fields.Integer(dump_only=True)
    conferenceId = fields.Integer(attribute="conference_id")
    name = fields.String(attribute="name", dump_only=True)


@swag.schema
class StadiumSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    nickname = fields.String()
    built = fields.Integer()
    capacity = fields.Integer()
    surface = fields.String()


@swag.schema
class TeamSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    shortName = fields.String(attribute='short_name', allow_none=True)
    mascot = fields.String()
    conferenceId = fields.Integer(attribute='conference_id', load_only=True)
    divisionId = fields.Integer(attribute='division_id')
    stadiumId = fields.Integer(attribute='stadium_id', allow_none=True)


@swag.schema
class GameParticipantSchema(Schema):
    id = fields.Integer(dump_only=True)
    teamId = fields.Integer(attribute='team_id')
    gameId = fields.Integer(attribute='game_id')
    locationTypeId = fields.Integer(attribute='location_type_id')
    score = fields.Integer(nullable=True, validate=score_validator)


@swag.schema
class GameSchema(Schema):
    id = fields.Integer(dump_only=True)
    kickoffTime = fields.DateTime(attribute='game_time',
                              validate=modern_datetime_validator)
    stadiumId = fields.Int(attribute='stadium_id')
    espnId = fields.Int(attribute='espn_id')
    participants: fields.Nested('GameParticipantSchema')


@swag.schema
class ScoreSchema(ma.Schema):
    teamId = fields.Integer(attribute="team_id")
    score = fields.Integer()

@swag.schema
class ErrorSchema(ma.Schema):
    code = fields.String()
    name = fields.String()
