from flask_restplus import Resource
import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.apis.api_v1 import api_manager
from hatchet.db.crud.games import list_games
from hatchet.apis.serializers import game, player
from hatchet.resources.schemas.schemas import TeamSchema
from hatchet.util import default_list_parser


ns_teams = api_manager.add_resource(
    name="teams",
    resource=db.Team,
    schema=TeamSchema,
    description="NCAA Football Teams representing a University",
    parser_args=["code"]
)
parser = default_list_parser(namespace=ns_teams)
parser.add_argument("code", type=str, required=False)
season_arg = ns_teams.parser()
season_arg.add_argument("season", type=int, required=False)



@ns_teams.route("/<int:id>/games")
@ns_teams.param("id", "the team identifier")
class TeamGames(Resource):
    @ns_teams.doc("get team games", parser=season_arg)
    @ns_teams.marshal_with(game)
    def get(self, id: int):
        args = season_arg.parse_args()
        season = int(args.get("season")) if args.get("season") else None
        games = list_games(team_id=id, season=season)
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


@ns_teams.route("/<int:id>/roster")
@ns_teams.param("id", "the team identifier")
class TeamRoster(Resource):
    @ns_teams.doc("get a Team's roster", parser=season_arg)
    @ns_teams.marshal_with(player)
    def get(self, id: int):
        args = season_arg.parse_args()
        team = queries.get_resource(id, db.Team)
        return team.roster(year=2018)