from marshmallow import post_load
from marshmallow.exceptions import ValidationError
from hatchet.extensions import ma, swag
from hatchet.db.models import (
    Conference, Division, Game, GameParticipant, Stadium, Team
)
from hatchet.api.schemas.validators import (
    modern_datetime_validator, modern_year_validator, score_validator
)


class HatchetSchema(ma.Schema):
    _Model = None

    def load_into(self, data, instance, many=False, partial=True):
        if "id" in data.keys():
            raise ValidationError("<id> is not a puttable fields")
        temp = self._do_load(data, many, partial=partial, postprocess=False)
        for k, v in temp.items():
            setattr(instance, k, v)
        return instance

    @post_load
    def make_object(self, data):
        return self._Model(**data)


@swag.definition('Conference', tags=['conferences'])
class ConferenceSchema(HatchetSchema):
    """
    A conference
    ---
    properties:
      id:
        type: integer
        format: int32
        example: 7
        readOnly: true
      code:
        type: string
        example: ACC
      name:
        type: string
        example: Atlantic Coast Conference
      inceptionYear:
        type: integer
        example: 1953
    """
    _Model = Conference
    id = ma.Int(dump_only=True)
    code = ma.Str()
    name = ma.Str()
    shortName = ma.Str(attribute='short_name', allow_none=True)
    inceptionYear = ma.Int(attribute="inception_year",
                           validate=modern_year_validator,
                           allow_none=True)


@swag.definition('Division', tags=['divisions'])
class DivisionSchema(HatchetSchema):
    """
    A division
    ---
    properties:
      id:
        type: integer
        format: int32
        example: 7
        readOnly: true
      conferenceId:
        type: integer
        format: int32
        example: 3
      name:
        type: string
        example: Atlantic
      fullName:
        type: string
        example: ACC Atlantic Division
    """
    _Model = Division
    id = ma.Int(dump_only=True)
    conferenceId = ma.Int(attribute='conference_id')
    name = ma.Str(allow_none=True)
    fullName = ma.Str(attribute='full_name', dump_only=True)


@swag.definition('Stadium', tags=['stadiums'])
class StadiumSchema(HatchetSchema):
    _Model = Stadium
    id = ma.Int(dump_only=True)
    name = ma.Str()
    nickname = ma.Str(allow_none=True)
    built = ma.Int()
    capacity = ma.Int()
    surface = ma.String(allow_none=True)


@swag.definition('Team', tags=['teams'])
class TeamSchema(HatchetSchema):
    """
    A team
    ---
    properties:
      id:
        type: integer
        format: int32
        example: 7
        readOnly: true
      name:
        type: string
        example: Clemson University
      shortName:
        type: string
        example: Clemson
      mascot:
        type: string
        example: Tigers
      conferenceId:
        type: integer
        format: int32
        example: 3
      divisionId:
        type: integer
        format: int32
        example: 12
      stadiumId:
        type: integer
        format: int32
        example: 43
    """
    _Model = Team
    id = ma.Int(nullable=True)
    name = ma.Str()
    shortName = ma.Str(attribute='short_name', allow_none=True)
    mascot = ma.Str()
    conferenceId = ma.Int(attribute='conference_id', allow_none=True)
    divisionId = ma.Int(attribute='division_id')
    stadiumId = ma.Int(attribute='stadium_id', allow_none=True)


@swag.definition("GameParticipant")
class GameParticipantSchema(HatchetSchema):
    """
    a game participant
    ---
    properties:
      id:
        type: integer
        format: int32
        example: 14
        readOnly: true
      teamId:
        type: integer
        format: int32
        example: 19
      gameId:
        type: integer
        format: int32
        example: 9
        readOnly: true
      locationTypeId:
        type: integer
        format: int32
        example: 1
      score:
        type: integer
        format: int32
        example: 44
      teamName:
        type: string
        example: Clemson
    """
    _Model = GameParticipant
    id = ma.Int(nullable=True)
    teamId = ma.Int(attribute='team_id')
    gameId = ma.Int(attribute='game_id')
    locationTypeId = ma.Int(attribute='location_type_id')
    score = ma.Int(nullable=True, validate=score_validator)
    teamName = ma.String(attribute='team.short_name', dump_only=True)


@swag.definition('Game', tags=['games'])
class GameSchema(HatchetSchema):
    """
    A game
    ---
    properties:
      id:
        type: integer
        format: int32
        example: 7
        readOnly: true
      kickoffTime:
        type: string
        format: datetime
        example: "2018-09-23T15:30:00-04:00"
      stadiumId:
        type: integer
        format: int32
        example: 45
      espnId:
        type: integer
        format: int32
        example: 9003245
      participants:
        type: array
        items:
          $ref: "#/definitions/GameParticipant"
    """
    _Model = Game
    id = ma.Int(nullable=True)
    #date = ma.Date(attribute='date', dump_only=True, nullable=True)
    kickoffTime = ma.DateTime(attribute='game_time',
                              validate=modern_datetime_validator)
    stadiumId = ma.Int(attribute='stadium_id')
    espnId = ma.Int(attribute='espn_id')

    participants = ma.Nested(GameParticipantSchema, many=True)


REGISTERED_SCHEMAS = [
    ConferenceSchema, DivisionSchema, StadiumSchema, TeamSchema, GameSchema,
    GameParticipantSchema
]

# __all__ = [ConferenceSchema, DivisionSchema, StadiumSchema, TeamSchema,
#            GameSchema]
