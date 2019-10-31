from flask_restplus import Resource, fields
import hatchet.db.models as db
import hatchet.db.meta_models as meta
import hatchet.db.crud.base as queries
from hatchet.apis.api_v1 import api_manager
from hatchet.db.crud.games import list_games
from hatchet.db.queries.lookups import lookup_team_by_external_id
from hatchet.apis.serializers import game, player, team, record
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

record_arg = ns_teams.parser()
record_arg.add_argument("season", type=int, required=False)


lookup = ns_teams.model("lookup", {
    "dataSource": fields.String(),
    "teamName": fields.String()
})


@ns_teams.route("/external/search")
class ExternalTeamLookup(Resource):
    @ns_teams.doc("lookup teams by an eternal identifier")
    @ns_teams.expect(lookup)
    @ns_teams.marshal_with(team)
    def post(self):
        data_source = ns_teams.payload.get("dataSource")
        identifier = ns_teams.payload.get("teamName")
        return lookup_team_by_external_id(data_source, identifier=identifier)


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


@ns_teams.route("/<int:id>/record")
@ns_teams.param("id", "the team identifier")
class TeamRecord(Resource):
    @ns_teams.doc("get a Team's record for a season", parser=record_arg)
    @ns_teams.marshal_with(record)
    def get(self, id: int):
        args = record_arg.parse_args()
        season = args.get("season", 2019)
        team = queries.get_resource(id, db.Team)
        return team.record(season=season)


@ns_teams.route("/<int:id>/roster")
@ns_teams.param("id", "the team identifier")
class TeamRoster(Resource):
    @ns_teams.doc("get a Team's roster", parser=season_arg)
    @ns_teams.marshal_with(player)
    def get(self, id: int):
        args = season_arg.parse_args()
        team = queries.get_resource(id, db.Team)
        return team.roster(year=2018)
