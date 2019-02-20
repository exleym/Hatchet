from flask import jsonify, request

from hatchet.api import api, api_response
from hatchet.db.crud.teams import (
    edit_team,
    list_teams,
    persist_team,
    remove_team_by_id
)


@api.route('/teams', methods=['POST'])
def create_team():
    team = persist_team(request.json)
    return api_response.dump(team, 201)


@api.route('/teams', methods=['GET'])
def get_teams():
    name = request.args.get("shortName", None)
    teams = list_teams(name=name)
    return api_response.dump(teams, 200)


@api.route('/teams/<int:team_id>', methods=['GET'])
def get_team_by_id(team_id: int):
    team = list_teams(team_id=team_id)
    return api_response.dump(team, 200)


@api.route('/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id: int):
    conf = edit_team(team_id=team_id, team=request.json)
    return api_response.dump(conf, 200)


@api.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id: int):
    remove_team_by_id(team_id=team_id)
    return jsonify(""), 204


@api.route('/teams/<int:team_id>/games', methods=['GET'])
def get_games_by_team(team_id: int):
    team = list_teams(team_id=team_id)
    return api_response.dump(team.games, 200)
