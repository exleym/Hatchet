from flask_restplus import fields
from hatchet.apis.api_v1 import api
import hatchet.resources.schemas.schemas as schemas
from hatchet.resources.schemas.converters import MarshmallowRestplusConverter


schema_converter = MarshmallowRestplusConverter(api=api)


coach = schema_converter.create_model(schemas.CoachSchema)
player = schema_converter.create_model(schemas.PlayerSchema)
subdivision = schema_converter.create_model(schemas.SubdivisionSchema)
surface = schema_converter.create_model(schemas.SurfaceSchema)
conference = schema_converter.create_model(schemas.ConferenceSchema)
division = schema_converter.create_model(schemas.DivisionSchema)
stadium = schema_converter.create_model(schemas.StadiumSchema)
team = schema_converter.create_model(schemas.TeamSchema)
participant = schema_converter.create_model(schemas.GameParticipantSchema)
game = schema_converter.create_model(schemas.GameSchema)


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