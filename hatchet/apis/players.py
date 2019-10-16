from flask_restplus import Namespace, Resource, fields

import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.apis.serializers import player, team
from hatchet.util import default_list_parser


ns = Namespace("players", description="player related operations")
parser = default_list_parser(namespace=ns)


@ns.route("")
class PlayerCollection(Resource):
    @ns.doc('list players', parser=parser)
    @ns.marshal_with(player)
    def get(self):
        args = parser.parse_args()
        return queries.list_resources(db.Player)

    @ns.expect(player)
    @ns.doc("create a new player")
    @ns.marshal_with(player)
    def post(self):
        return queries.persist_resource(ns.payload, db.Player)


@ns.route("/<int:id>")
@ns.response(404, 'Player not found')
@ns.param('id', 'The player identifier')
class Player(Resource):
    @ns.doc("get player by id")
    @ns.marshal_with(player)
    def get(self, id: int):
        return queries.get_resource(id, db.Player)

    @ns.expect(player)
    @ns.doc("update player")
    @ns.marshal_with(player)
    def put(self, id: int):
        return queries.edit_resource(id, ns.payload, db.Player)

    @ns.doc("delete player")
    @ns.response(204, "player deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Player)
        return ""
