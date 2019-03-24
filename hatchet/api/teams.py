from flask import jsonify, request
from flasgger import swag_from

from hatchet.api import api, api_response
from hatchet.db.crud.teams import (
    edit_team,
    list_teams,
    persist_team,
    remove_team_by_id
)

flasgger_team = '../static/swagger/paths/teams'


@api.route('/teams', methods=['POST'])
@swag_from(f"{flasgger_team}/create_team.yml")
def create_team():
    team = persist_team(request.json)
    return api_response.dump(team, 201)


@api.route('/teams', methods=['GET'])
@swag_from(f"{flasgger_team}/list_teams.yml")
def get_teams():
    name = request.args.get("shortName", None)
    teams = list_teams(name=name)
    return api_response.dump(teams, 200)


@api.route('/teams/<int:team_id>', methods=['GET'])
@swag_from(f"{flasgger_team}/get_team_by_id.yml")
def get_team_by_id(team_id: int):
    team = list_teams(team_id=team_id)
    return api_response.dump(team, 200)


@api.route('/teams/<int:team_id>', methods=['PUT'])
@swag_from(f"{flasgger_team}/update_team.yml")
def update_team(team_id: int):
    conf = edit_team(team_id=team_id, team=request.json)
    return api_response.dump(conf, 200)


@api.route('/teams/<int:team_id>', methods=['DELETE'])
@swag_from(f"{flasgger_team}/delete_team.yml")
def delete_team(team_id: int):
    remove_team_by_id(team_id=team_id)
    return jsonify(""), 204


@api.route('/teams/<int:team_id>/games', methods=['GET'])
@swag_from(f"{flasgger_team}/get_team_games.yml")
def get_games_by_team(team_id: int):
    team = list_teams(team_id=team_id)
    return api_response.dump(team.games, 200)
