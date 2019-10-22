from flask import Blueprint
from flask_restplus import Api
from hatchet.autocrud.api_manager import APIManager
import hatchet.resources.schemas.schemas as schemas


blueprint = Blueprint("api", __name__)


api = Api(
    blueprint,
    title="Hatchet API",
    version="1.0",
    description="API for managing Hatchet CFB data"
)

api_manager = APIManager(title="demo", version="1.0", api=api)

from hatchet.apis.subdivisions import ns_subdivisions
from hatchet.apis.conferences import ns_conferences
from hatchet.apis.divisions import ns_divisions
from hatchet.apis.teams import ns_teams
from hatchet.apis.games import ns as ns_games
from hatchet.apis.stadiums import ns as ns_stadiums
from hatchet.apis.coaches import ns as ns_coaches
from hatchet.apis.players import ns as ns_players
from hatchet.apis.data_sources import ns as ns_data_sources


api.add_namespace(ns_games)
api.add_namespace(ns_stadiums)
api.add_namespace(ns_coaches)
api.add_namespace(ns_players)
api.add_namespace(ns_data_sources)


from hatchet.db.models import Bookmaker
from hatchet.resources.schemas.schemas import BookmakerSchema

api_manager.add_resource("bookmakers", Bookmaker, BookmakerSchema, "bookmaker resources")
