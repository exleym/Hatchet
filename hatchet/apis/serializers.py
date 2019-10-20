from flask_restplus import fields
from hatchet.apis.api_v1 import api
from hatchet.resources.schemas.schemas import SubdivisionSchema
from hatchet.resources.schemas.converters import restplus_model_from_schema


# subdivision = api.model("Subdivision", {
#     "id": fields.Integer(),
#     "code": fields.String(),
#     "name": fields.String(),
#     "division": fields.Integer()
# })
subdivision = api.model("Subdivision", restplus_model_from_schema(SubdivisionSchema))


conference = api.model("Conference", {
    "id": fields.Integer(),
    "subdivisionId": fields.Integer(attribute="subdivision_id"),
    "code": fields.String(),
    "name": fields.String(),
    "shortName": fields.String(attribute="short_name"),
    "inceptionYear": fields.Integer(attribute="inception_year"),
    "subdivision": fields.Nested(model=subdivision)
}, mask="{id,subdivisionId,code,name,shortName,inceptionYear}")


coach = api.model("Coach", {
    "id": fields.Integer(),
    "firstName": fields.String(attribute="first_name"),
    "lastName": fields.String(attribute="last_name"),
    "dateOfBirth": fields.Date(attribute="dob")
})


player = api.model("Coach", {
    "id": fields.Integer(),
    "firstName": fields.String(attribute="first_name"),
    "lastName": fields.String(attribute="last_name"),
    "dateOfBirth": fields.Date(attribute="dob")
})


surface = api.model("Surface", {
    "id": fields.Integer(),
    "code": fields.String(),
    "name": fields.String(),
    "category": fields.String()
})


stadium = api.model("Stadium", {
    "id": fields.Integer(),
    "code": fields.String(),
    "name": fields.String(),
    "state": fields.String(),
    "city": fields.String(),
    "latitude": fields.String(),
    "longitude": fields.String(),
    "built": fields.Integer(),
    "capacity": fields.Integer(),
    "surfaceId": fields.String(attribute="surface_id"),
    "surface": fields.Nested(surface)
}, mask="{surface{name,category},*}")


division = api.model("Division", {
    "id": fields.Integer(),
    "conferenceId": fields.Integer(attribute="conference_id"),
    "name": fields.String(),
    "conference": fields.Nested(conference, skip_none=True)
}, mask="{id,conferenceId,name}")


team = api.model("Team", {
    "id": fields.Integer(),
    "code": fields.String(),
    "name": fields.String(),
    "shortName": fields.String(attribute="short_name"),
    "mascot": fields.String(),
    "conferenceId": fields.Integer(attribute="conference_id"),
    "divisionId": fields.Integer(attribute="division_id"),
    "stadiumId": fields.Integer(attribute="stadium_id"),
    "stadium": fields.Nested(stadium),
    "conference": fields.Nested(conference),
    "division": fields.Nested(division)
},mask="{id,code,name,shortName,mascot,conferenceId,divisionId,stadiumId}")


game_participant = api.model("GameParticipant", {
    "id": fields.Integer(),
    "teamId": fields.Integer(attribute="team_id"),
    "gameId": fields.Integer(attribute="game_id"),
    "locationTypeId": fields.Integer(attribute="location_type_id"),
    "score": fields.Integer(),
    "team": fields.Nested(team, skip_none=True)
})


game = api.model("Game", {
    "id": fields.Integer(required=False),
    "kickoffTime": fields.DateTime(attribute="game_time"),
    "stadiumId": fields.Integer(),
    "espnId": fields.Integer(required=False),
    "participants": fields.Nested(game_participant, skip_none=True, required=False),
    "winner": fields.Nested(game_participant, skip_none=True, required=False)
})
# game = api.model("Game", restplus_model_from_schema(GameSchema))


play = api.model("Play", {
    "id": fields.Integer(),
    "quarter": fields.Integer(),
    "playNumber": fields.Integer(attribute="play_number"),
    "gameClock": fields.String(attribute="game_clock"),
    "gameId": fields.Integer(attribute="game_id"),
    "down": fields.Integer(),
    "toGo": fields.Float(attribute="to_go"),
    "playOccurred": fields.Boolean(attribute="play_occurred"),
    "penaltyOccurred": fields.Boolean(attribute="penalty_occurred")
})


data_source = api.model("DataSource", {
    "id": fields.Integer(),
    "name": fields.String(max_length=128),
    "url": fields.String(max_length=255)
})