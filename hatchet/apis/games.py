from flask_restplus import Namespace, Resource, fields

import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.apis.serializers import game, play
from hatchet.util import default_list_parser


ns = Namespace("games", description="game related operations")
parser = default_list_parser(namespace=ns)


@ns.route("/")
class GameCollection(Resource):
    @ns.doc('list games', parser=parser)
    @ns.marshal_with(game)
    def get(self):
        args = parser.parse_args()
        return queries.list_resources(db.Game)

    @ns.expect(game)
    @ns.doc("create a new game")
    @ns.marshal_with(game)
    def post(self):
        return queries.persist_resource(ns.payload, db.Game)


@ns.route("/<int:id>")
@ns.response(404, 'Game not found')
@ns.param('id', 'The game identifier')
class Game(Resource):
    @ns.doc("get game by id")
    @ns.marshal_with(game)
    def get(self, id: int):
        return queries.get_resource(id, db.Game)

    @ns.expect(game)
    @ns.doc("update game")
    @ns.marshal_with(game)
    def put(self, id: int):
        return queries.edit_resource(id, ns.payload, db.Game)

    @ns.doc("delete game")
    @ns.response(204, "game deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Game)
        return ""


@ns.route("/<int:id>/plays")
@ns.param("id", "the game identifier")
class GamePlays(Resource):
    @ns.doc("get plays in a game")
    @ns.marshal_with(play)
    def get(self, id: int):
        game = queries.get_resource(id, db.Game)
        return game.plays
