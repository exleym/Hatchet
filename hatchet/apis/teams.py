import datetime as dt
from flask_restplus import Resource, fields, inputs
import logging
import hatchet.db.models as db
import hatchet.db.meta_models as mm
import hatchet.db.crud.games as game_queries
import hatchet.db.crud.base as queries
from hatchet.apis.api_v1 import api_manager
from hatchet.db.queries.lookups import lookup_team_by_external_id
from hatchet.apis.serializers import game, player, team, record
from hatchet.resources.schemas.schemas import TeamSchema
from hatchet.util import default_list_parser


logger = logging.getLogger(__name__)
ns_teams = api_manager.add_resource(
    name="teams",
    resource=db.Team,
    schema=TeamSchema,
    description="NCAA Football Teams representing a University",
    parser_args=["code", "name", "short_name"]
)
parser = default_list_parser(namespace=ns_teams)
parser.add_argument("code", type=str, required=False)

team_games_args = ns_teams.parser()
team_games_args.add_argument("season", type=int, required=False)
team_games_args.add_argument("date", type=inputs.date_from_iso8601, required=False)

season_arg = ns_teams.parser()
season_arg.add_argument("season", type=int, required=False)

record_arg = ns_teams.parser()
record_arg.add_argument("season", type=int, required=False)

ext_map_arg = ns_teams.parser()
ext_map_arg.add_argument("sourceId", type=int, required=False)
ext_map_arg.add_argument("teamId", type=int, required=False)


lookup = ns_teams.model("lookup", {
    "dataSource": fields.String(),
    "teamName": fields.String()
})

external_mapping = ns_teams.model("external_mapping", {
    "dataSource": fields.String(attribute="source.name", dump_only=True),
    "sourceId": fields.Integer(attribute="source_id", load_only=True),
    "teamName": fields.String(attribute="value"),
    "externalId": fields.Integer(attribute="external_id"),
    "teamId": fields.Integer(attribute="team_id")
})


@ns_teams.route("/external/mapping")
class ExternalTeamMappings(Resource):
    @ns_teams.doc("create an external mapping")
    @ns_teams.expect(external_mapping)
    @ns_teams.marshal_with(external_mapping)
    def post(self):
        return None

    @ns_teams.doc("list external mappings")
    @ns_teams.param("sourceId", "external dataSource to filter")
    @ns_teams.param("teamId", "external dataSource to filter")
    @ns_teams.marshal_with(external_mapping)
    def get(self):
        args = ext_map_arg.parse_args()
        params = {}
        params.update(args)
        print(args)
        return queries.list_resources(mm.ExternalTeamIdentifier, **params)



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
    @ns_teams.doc("get team games", parser=team_games_args)
    @ns_teams.marshal_with(game)
    def get(self, id: int):
        args = team_games_args.parse_args()
        season = int(args.get("season")) if args.get("season") else None
        date = args.get("date")
        games = game_queries.list_games(team_id=id, season=season, date=date)
        return games


@ns_teams.route("/<int:id>/record")
@ns_teams.param("id", "the team identifier")
class TeamRecord(Resource):
    @ns_teams.doc("get a Team's record for a season", parser=record_arg)
    @ns_teams.marshal_with(record)
    def get(self, id: int):
        args = record_arg.parse_args()
        season = args.get("season") or 2019
        print(season)
        return game_queries.get_team_record_by_season(team_id=id, season=season)


@ns_teams.route("/<int:id>/roster")
@ns_teams.param("id", "the team identifier")
class TeamRoster(Resource):
    @ns_teams.doc("get a Team's roster", parser=season_arg)
    @ns_teams.marshal_with(player)
    def get(self, id: int):
        args = season_arg.parse_args()
        team = queries.get_resource(id, db.Team)
        return team.roster(year=2018)
