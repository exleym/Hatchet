from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint("api", __name__)


api = Api(
    blueprint,
    title="Hatchet API",
    version="1.0",
    description="API for managing Hatchet CFB data"
)


from hatchet.apis.subdivisions import ns as ns_subdivisions
from hatchet.apis.conferences import ns as ns_conferences
from hatchet.apis.divisions import ns as ns_divisions
from hatchet.apis.teams import ns as ns_teams
from hatchet.apis.games import ns as ns_games
from hatchet.apis.stadiums import ns as ns_stadiums
from hatchet.apis.coaches import ns as ns_coaches
from hatchet.apis.players import ns as ns_players


api.add_namespace(ns_subdivisions)
api.add_namespace(ns_conferences)
api.add_namespace(ns_divisions)
api.add_namespace(ns_teams)
api.add_namespace(ns_games)
api.add_namespace(ns_stadiums)
api.add_namespace(ns_coaches)
api.add_namespace(ns_players)
