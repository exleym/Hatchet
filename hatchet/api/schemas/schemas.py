from marshmallow import post_load
from hatchet.extensions import ma
from hatchet.db.models import (
    Conference, Division, Game, GameParticipant, Stadium, Team
)
from hatchet.api.schemas.validators import (
    modern_datetime_validator, modern_year_validator, score_validator
)


class HatchetSchema(ma.Schema):
    _Model = None

    @post_load
    def make_object(self, data):
        return self._Model(**data)


class ConferenceSchema(HatchetSchema):
    _Model = Conference
    id = ma.Int(dump_only=True)
    code = ma.Str()
    name = ma.Str()
    shortName = ma.Str(attribute='short_name', allow_none=True)
    inceptionYear = ma.Int(attribute="inception_year",
                           validate=modern_year_validator,
                           allow_none=True)


class DivisionSchema(HatchetSchema):
    _Model = Division
    id = ma.Int(dump_only=True)
    conferenceId = ma.Int(attribute='conference_id')
    name = ma.Str(allow_none=True)
    fullName = ma.Str(attribute='full_name', dump_only=True)


class StadiumSchema(HatchetSchema):
    _Model = Stadium
    id = ma.Int(dump_only=True)
    name = ma.Str()
    nickname = ma.Str(allow_none=True)
    built = ma.Int()
    capacity = ma.Int()
    surface = ma.String(allow_none=True)


class TeamSchema(HatchetSchema):
    _Model = Team
    id = ma.Int(nullable=True)
    name = ma.Str()
    shortName = ma.Str(attribute='short_name', allow_none=True)
    mascot = ma.Str()
    conferenceId = ma.Int(attribute='conference_id', load_only=True)
    divisionId = ma.Int(attribute='division_id')
    stadiumId = ma.Int(attribute='stadium_id', allow_none=True)


class GameParticipantSchema(HatchetSchema):
    _Model = GameParticipant
    id = ma.Int(nullable=True)
    teamId = ma.Int(attribute='team_id')
    gameId = ma.Int(attribute='game_id')
    locationTypeId = ma.Int(attribute='location_type_id')
    score = ma.Int(nullable=True, validate=score_validator)


class GameSchema(HatchetSchema):
    _Model = Game
    id = ma.Int(nullable=True)
    #date = ma.Date(attribute='date', dump_only=True, nullable=True)
    kickoffTime = ma.DateTime(attribute='game_time',
                              validate=modern_datetime_validator)
    stadiumId = ma.Int(attribute='stadium_id')

    participants = ma.Nested(GameParticipantSchema, many=True)


REGISTERED_SCHEMAS = [
    ConferenceSchema, DivisionSchema, StadiumSchema, TeamSchema, GameSchema,
    GameParticipantSchema
]

# __all__ = [ConferenceSchema, DivisionSchema, StadiumSchema, TeamSchema,
#            GameSchema]
