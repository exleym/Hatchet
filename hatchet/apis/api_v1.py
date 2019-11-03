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

import hatchet.apis.subdivisions
import hatchet.apis.conferences
import hatchet.apis.divisions
import hatchet.apis.teams
import hatchet.apis.games
import hatchet.apis.stadiums
import hatchet.apis.coaches
import hatchet.apis.players
import hatchet.apis.data_sources
import hatchet.apis.bookmakers
import hatchet.apis.lines
import hatchet.apis.weeks
import hatchet.apis.polls
