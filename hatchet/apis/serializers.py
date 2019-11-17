from flask_restplus import fields

from hatchet.apis.api_v1 import api
import hatchet.resources.schemas.schemas as schemas
from hatchet.apis.api_v1 import api_manager


coach = api_manager.create_model(schemas.CoachSchema)
player = api_manager.create_model(schemas.PlayerSchema)
subdivision = api_manager.create_model(schemas.SubdivisionSchema)
surface = api_manager.create_model(schemas.SurfaceSchema)
conference = api_manager.create_model(schemas.ConferenceSchema)
division = api_manager.create_model(schemas.DivisionSchema)
stadium = api_manager.create_model(schemas.StadiumSchema)
team = api_manager.create_model(schemas.TeamSchema)
participant = api_manager.create_model(schemas.GameParticipantSchema)
network = api_manager.create_model(schemas.NetworkSchema)
rating = api_manager.create_model(schemas.RatingSchema)
game = api_manager.create_model(schemas.GameSchema)
search = api_manager.create_model(schemas.SearchSchema)
poll = api_manager.create_model(schemas.PollSchema)
ranking = api_manager.create_model(schemas.RankingSchema)
week = api_manager.create_model(schemas.WeekSchema)


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


record = api.model("Record", {
    "season": fields.Integer(),
    "wins": fields.Integer(),
    "losses": fields.Integer(),
    "confWins": fields.Integer(),
    "confLosses": fields.Integer()
})