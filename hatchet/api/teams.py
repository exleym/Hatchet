from flask import jsonify, request
from flasgger import swag_from

from hatchet.api import api
from hatchet.api.schemas.schemas import (
    GameSchema,
    TeamSchema,
)
from hatchet.db.crud.teams import (
    edit_team,
    list_teams,
    persist_team,
    remove_team_by_id
)

game_schema = GameSchema()
team_schema = TeamSchema()


def swag_path(context):
    SWAGGER_PATH = "../static/swagger/teams"
    return SWAGGER_PATH + context


@api.route('/teams', methods=['POST'])
@swag_from(swag_path('/create_team.yml'))
def create_team():
    team = persist_team(request.json)
    return jsonify(team_schema.dump(team)), 201


@api.route('/teams', methods=['GET'])
@swag_from(swag_path("/get_teams.yml"))
def get_teams():
    name = request.args.get("shortName", None)
    teams = list_teams(name=name)
    return jsonify(team_schema.dump(teams, many=True)), 200


@api.route('/teams/<int:team_id>', methods=['GET'])
@swag_from(swag_path('/get_team_by_id.yml'))
def get_team_by_id(team_id: int):
    team = list_teams(team_id=team_id)
    return jsonify(team_schema.dump(team)), 200


@api.route('/teams/<int:team_id>', methods=['PUT'])
@swag_from(swag_path("/update_team.yml"))
def update_team(team_id: int):
    team = edit_team(team_id=team_id, team=request.json)
    return jsonify(team_schema.dump(team)), 200


@api.route('/teams/<int:team_id>', methods=['DELETE'])
@swag_from(swag_path("/delete_team.yml"))
def delete_team(team_id: int):
    remove_team_by_id(team_id=team_id)
    return jsonify(""), 204


@api.route('/teams/<int:team_id>/games', methods=['GET'])
@swag_from(swag_path("/get_games_by_team.yml"))
def get_games_by_team(team_id: int):
    team = list_teams(team_id=team_id)
    return jsonify(game_schema.dump(team.games)), 200
