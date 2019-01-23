from flask import jsonify, request

from hatchet.api import api, api_response
from hatchet.db.crud.games import (
    edit_game,
    list_games,
    persist_game,
    remove_game_by_id,
    make_participant,
    update_score
)


@api.route('/games', methods=['POST'])
def create_game():
    game = persist_game(request.json)
    return api_response.dump(game, 201)


@api.route('/games', methods=['GET'])
def get_games():
    games = list_games()
    return api_response.dump(games, 200)


@api.route('/games/<int:game_id>', methods=['GET'])
def get_game_by_id(game_id: int):
    game = list_games(game_id=game_id)
    return api_response.dump(game, 200)


@api.route('/games/<int:game_id>', methods=['PUT'])
def update_game(game_id: int):
    conf = edit_game(game_id=game_id, game=request.json)
    return api_response.dump(conf, 200)


@api.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id: int):
    remove_game_by_id(game_id=game_id)
    return jsonify(""), 204


@api.route('/games/<int:game_id>/participants', methods=['GET'])
def get_game_participants(game_id: int):
    game = list_games(game_id=game_id)
    return api_response.dump(game.participants, 200)


@api.route('/games/<int:game_id>/participants', methods=['POST'])
def add_game_participant(game_id: int):
    game = get_game_by_id(game_id)  # validate that game actually exists
    if len(game.participants) >= 2:
        raise ValueError("maxiumum of 2 participants per game")
    participant = make_participant(request.json)
    return api_response.dump(participant, 201)


@api.route('/games/<int:game_id>/scores', methods=['POST'])
def add_score(game_id: int):
    game = update_score(game_id, request.json)
    return api_response.dump(game, 201)
