from flask import current_app, jsonify, request
from flasgger import swag_from
from marshmallow import ValidationError

from hatchet.api import api, api_response
from hatchet.db.crud.games import (
    edit_game,
    list_games,
    persist_game,
    remove_game_by_id,
    make_participant,
    update_score
)

flasgger_game = '../static/swagger/paths/games'


@api.route('/games', methods=['POST'])
@swag_from(f"{flasgger_game}/create_game.yml")
def create_game():
    game = persist_game(request.json)
    return api_response.dump(game, 201)


@api.route('/games', methods=['GET'])
@swag_from(f"{flasgger_game}/list_games.yml")
def get_games():
    games = list_games()
    return api_response.dump(games, 200)


@api.route('/games/<int:game_id>', methods=['GET'])
@swag_from(f"{flasgger_game}/get_game_by_id.yml")
def get_game_by_id(game_id: int):
    game = list_games(game_id=game_id)
    return api_response.dump(game, 200)


@api.route('/games/<int:game_id>', methods=['PUT'])
@swag_from(f"{flasgger_game}/update_game.yml")
def update_game(game_id: int):
    game = edit_game(game_id=game_id, game=request.json, partial=False)
    return api_response.dump(game, 200)


@api.route('/games/<int:game_id>', methods=['PATCH'])
@swag_from(f"{flasgger_game}/patch_game.yml")
def patch_game(game_id: int):
    game = edit_game(game_id=game_id, game=request.json, partial=True)
    return api_response.dump(game, 200)


@api.route('/games/<int:game_id>', methods=['DELETE'])
@swag_from(f"{flasgger_game}/delete_game.yml")
def delete_game(game_id: int):
    remove_game_by_id(game_id=game_id)
    return jsonify(""), 204


@api.route('/games/<int:game_id>/participants', methods=['GET'])
@swag_from(f"{flasgger_game}/get_game_participants.yml")
def get_game_participants(game_id: int):
    game = list_games(game_id=game_id)
    return api_response.dump(game.participants, 200)


@api.route('/games/<int:game_id>/participants', methods=['POST'])
@swag_from(f"{flasgger_game}/add_game_participant.yml")
def add_game_participant(game_id: int):
    game = list_games(game_id=game_id)  # validate that game actually exists
    if len(game.participants) >= 2:
        current_app.logger.error(f'request to add third participant to {game}')
        raise ValidationError(message="maxiumum of 2 participants per game")
    participant = make_participant(request.json)
    return api_response.dump(participant, 201)


@api.route('/games/<int:game_id>/scores', methods=['POST'])
@swag_from(f"{flasgger_game}/add_score.yml")
def add_score(game_id: int):
    game = update_score(game_id, request.json)
    return api_response.dump(game, 201)
