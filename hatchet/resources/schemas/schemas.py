from flask_filter.schemas import vali1date_operator
from marshmallow import fields, Schema

from hatchet.resources.schemas.validators import (
    modern_datetime_validator, modern_year_validator, score_validator
)
from hatchet.resources.schemas.base import BaseSchema


class BookmakerSchema(BaseSchema):
    code = fields.String(example="BOV")
    name = fields.String(example="Bovada")
    website = fields.String(example="http://www.bovada.lv")


class CoachSchema(BaseSchema):
    firstName = fields.String(attribute="first_name")
    lastName = fields.String(attribute="last_name")
    dateOfBirth = fields.Date(attribute="dob")


class ConferenceSchema(BaseSchema):
    subdivisionId = fields.Integer(attribute="subdivision_id")
    code = fields.String()
    name = fields.String()
    shortName = fields.String(attribute="short_name")
    inceptionYear = fields.Integer (
        attribute="inception_year",
        validate=modern_year_validator,
        allow_none=True
    )
    subdivision =fields.Nested("SubdivisionSchema")


class DivisionSchema(BaseSchema):
    conferenceId = fields.Integer(attribute="conference_id")
    name = fields.String(attribute="name")
    conference = fields.Nested("ConferenceSchema", allow_none=True)


class ErrorSchema(BaseSchema):
    code = fields.String()
    name = fields.String()


class GameParticipantSchema(BaseSchema):
    teamId = fields.Integer(attribute='team_id')
    gameId = fields.Integer(attribute='game_id')
    locationTypeId = fields.Integer(attribute='location_type_id')
    score = fields.Integer(validate=score_validator, allow_none=True)
    team = fields.Nested(
        'TeamSchema',
        many=False,
        exclude=["stadium"]
    )


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
    rating = fields.Nested("RatingSchema", allow_none=True, required=False,
                           many=False)


class LineSchema(BaseSchema):
    gameId = fields.Integer(attribute="game_id")
    teamId = fields.Integer(attribute="team_id")
    bookmakerId = fields.Integer(attribute="bookmaker_id")
    spread = fields.Float(allow_none=True)
    overUnder = fields.Float(attribute="over_under", allow_none=True)
    vigorish = fields.Integer(allow_none=True)


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
    logo = fields.String(required=False, allow_none=True)
    conferenceId = fields.Integer(attribute='conference_id')
    divisionId = fields.Integer(attribute='division_id')
    stadiumId = fields.Integer(attribute='stadium_id', allow_none=True)
    stadium = fields.Nested("StadiumSchema", dump_only=True)
    #conference = fields.Nested("ConferenceSchema", dump_only=True)
    division = fields.Nested("DivisionSchema", dump_only=True)


class PostFilterSchema(Schema):
    field = fields.String(required=True, allow_none=False)
    op = fields.String(required=True, attribute="OP", validate=vali1date_operator)
    value = fields.Field(required=True, allow_none=False)


class SearchSchema(Schema):
    filters = fields.List(fields.Nested("PostFilterSchema"))


class PollSchema(BaseSchema):
    code = fields.String()
    name = fields.String()
    url = fields.String()


class RankingSchema(BaseSchema):
    weekId = fields.Integer(attribute="week_id")
    pollId = fields.Integer(attribute="poll_id")
    teamId = fields.Integer(attribute="team_id")
    rank = fields.Integer()
    priorRank = fields.Integer(attribute="prior_rank")
    poll = fields.Nested("PollSchema")
    team = fields.Nested("TeamSchema")


class WeekSchema(BaseSchema):
    number = fields.Integer()
    season = fields.Integer()
    startDate = fields.Date(attribute="start_date")
    endDate = fields.Date(attribute="end_date")


class DataSourceSchema(BaseSchema):
    code = fields.String()
    name = fields.String()
    url = fields.String()


class NetworkSchema(BaseSchema):
    code = fields.String()
    name = fields.String()
    website = fields.String(allow_none=True, required=False)


class RatingSchema(BaseSchema):
    gameId = fields.Integer(attribute="game_id")
    networkId = fields.Integer(attribute="network_id")
    rating = fields.Float(required=False, allow_none=True)
    viewers = fields.Float(required=False, allow_none=True)
