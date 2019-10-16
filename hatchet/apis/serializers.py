from flask_restplus import fields
from hatchet.apis.api_v1 import api


conference = api.model("Conference", {
    "id": fields.Integer(),
    "code": fields.String(),
    "name": fields.String(),
    "shortName": fields.String(attribute="short_name"),
    "inceptionYear": fields.Integer(attribute="inception_year")
})


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


stadium = api.model("Stadium", {
    "id": fields.Integer(),
    "name": fields.String(),
    "nickname": fields.String(),
    "built": fields.Integer(),
    "capacity": fields.Integer(),
    "surface": fields.String()
})


division = api.model("Division", {
    "id": fields.Integer(),
    "conferenceId": fields.Integer(attribute="conference_id"),
    "name": fields.String(),
    "conference": fields.Nested(conference, skip_none=True)
})


team = api.model("Team", {
    "id": fields.Integer(),
    "name": fields.String(),
    "shortName": fields.String(attribute="short_name"),
    "mascot": fields.String(),
    "conferenceId": fields.Integer(attribute="conference_id"),
    "divisionId": fields.Integer(attribute="division_id"),
    "stadiumId": fields.Integer(attribute="stadium_id")
})


game_participant = api.model("GameParticipant", {
    "id": fields.Integer(),
    "teamId": fields.Integer(attribute="team_id"),
    "gameId": fields.Integer(attribute="game_id"),
    "locationTypeId": fields.Integer(attribute="location_type_id"),
    "score": fields.Integer(),
    "team": fields.Nested(team, skip_none=True)
})


game = api.model("Game", {
    "id": fields.Integer(),
    "kickoffTime": fields.DateTime(attribute="game_time"),
    "stadiumId": fields.Integer(),
    "espnId": fields.Integer(),
    "participants": fields.Nested(game_participant, skip_none=True),
    "winner": fields.Nested(game_participant, skip_none=True)
})


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