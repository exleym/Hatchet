from flask_restplus import Namespace, Resource, fields

import hatchet.db.models as db
from hatchet.resources.schemas.schemas import GameSchema
from hatchet.apis.api_v1 import api_manager

import hatchet.db.models as models
import hatchet.db.crud.base as queries
from hatchet.resources.schemas.schemas import GameSchema, GameParticipantSchema
from hatchet.apis.serializers import game, play
from hatchet.util import default_list_parser, camel_to_snake


ns_games = api_manager.add_resource(
    name="games",
    resource=db.Game,
    schema=GameSchema,
    description="manage games"
)


# @ns_games.route("")
# class GameCollection(Resource):
#     @ns_games.doc('list games', parser=parser)
#     @ns_games.marshal_with(game)
#     def get(self):
#         args = parser.parse_args()
#         return queries.list_resources(models.Game)
# 
#     @ns_games.expect(game)
#     @ns_games.doc("create a new game", parser=parser)
#     @ns_games.marshal_with(game)
#     def post(self):
#         data = game_schema.load(ns_games.payload)
#         participants = [
#             models.GameParticipant(**gp)
#             for gp in data.pop("participants", [])
#         ]
#         game = models.Game(**data)
#         for p in participants:
#             game.participants.append(p)
#         db.session.add(game)
#         db.session.commit()
#         return game


@ns_games.route("/<int:id>/plays")
@ns_games.param("id", "the game identifier")
class GamePlays(Resource):
    @ns_games.doc("get plays in a game")
    @ns_games.marshal_with(play)
    def get(self, id: int):
        game = queries.get_resource(id, models.Game)
        return game.plays
