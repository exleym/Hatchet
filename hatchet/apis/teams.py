from flask_restplus import Namespace, Resource, fields
import logging

import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.db.crud.games import list_games
from hatchet.apis.serializers import team, game, player
from hatchet.util import default_list_parser


logger = logging.getLogger(__name__)
ns = Namespace("teams", description="team related operations")
parser = default_list_parser(namespace=ns)
parser.add_argument("code", type=str, required=False)


season_arg = ns.parser()
season_arg.add_argument("season", type=int, required=False)




@ns.route("")
class TeamCollection(Resource):
    @ns.doc('list teams', parser=parser)
    @ns.marshal_with(team)
    def get(self):
        args = parser.parse_args()
        return queries.list_resources(db.Team, code=args.get("code"))

    @ns.expect(team)
    @ns.doc("create a new team")
    @ns.marshal_with(team)
    def post(self):
        return queries.persist_resource(ns.payload, db.Team)


@ns.route("/<int:id>")
@ns.response(404, 'Team not found')
@ns.param('id', 'The team identifier')
class Team(Resource):
    @ns.doc("get team by id")
    @ns.marshal_with(team)
    def get(self, id: int):
        return queries.get_resource(id, db.Team)

    @ns.expect(team)
    @ns.doc("update team")
    @ns.marshal_with(team)
    def put(self, id: int):
        return queries.edit_resource(id, ns.payload, db.Team)

    @ns.doc("delete team")
    @ns.response(204, "team deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Team)
        return ""


@ns.route("/<int:id>/games")
@ns.param("id", "the team identifier")
class TeamGames(Resource):
    @ns.doc("get team games", parser=season_arg)
    @ns.marshal_with(game)
    def get(self, id: int):
        args = season_arg.parse_args()
        logger.info(args)
        season = int(args.get("season")) if args.get("season") else None
        logger.info(season)
        games = list_games(team_id=id, season=season)
        logger.info(games)
        return games
        # team = queries.get_resource(id, db.Team)
        # games = team.games
        # games.sort(key=lambda x: x.game_time)
        # if not season:
        #     return games
        # return [
        #     g for g in games
        #     if g.game_time.date().year == season
        # ]


@ns.route("/<int:id>/roster")
@ns.param("id", "the team identifier")
class TeamRoster(Resource):
    @ns.doc("get a Team's roster", parser=season_arg)
    @ns.marshal_with(player)
    def get(self, id: int):
        args = season_arg.parse_args()
        team = queries.get_resource(id, db.Team)
        return team.roster(year=2018)