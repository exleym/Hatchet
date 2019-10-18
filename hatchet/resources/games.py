from flask import current_app, jsonify, request
from flasgger import swag_from
from marshmallow import ValidationError

from hatchet.resources import api
from hatchet.apis.schemas import (
    GameSchema,
    GameParticipantSchema,
)
from hatchet.db.crud.games import (
    edit_game,
    list_games,
    persist_game,
    remove_game_by_id,
    make_participant,
    update_score
)


game_schema = GameSchema()
game_participant_schema = GameParticipantSchema()


def swag_path(context):
    SWAGGER_PATH = "../static/swagger/games"
    return SWAGGER_PATH + context


@api.route('/games', methods=['POST'])
@swag_from(swag_path("/create_game.yml"))
def create_game():
    game = persist_game(request.json)
    return jsonify(game_schema.dump(game)), 201


@api.route('/games', methods=['GET'])
@swag_from(swag_path("/get_games.yml"))
def get_games():
    games = list_games()
    return jsonify(game_schema.dump(games, many=True)), 200


@api.route('/games/<int:game_id>', methods=['GET'])
@swag_from(swag_path('/get_game_by_id.yml'))
def get_game_by_id(game_id: int):
    game = list_games(game_id=game_id)
    return jsonify(game_schema.dump(game)), 200


@api.route('/games/<int:game_id>', methods=['PUT'])
@swag_from(swag_path("/update_game.yml"))
def update_game(game_id: int):
    game = edit_game(game_id=game_id, game=request.json)
    return jsonify(game_schema.dump(game)), 200


@api.route('/games/<int:game_id>', methods=['DELETE'])
@swag_from(swag_path("/delete_game.yml"))
def delete_game(game_id: int):
    remove_game_by_id(game_id=game_id)
    return jsonify(""), 204


@api.route('/games/<int:game_id>/participants', methods=['GET'])
@swag_from(swag_path("/get_game_participants.yml"))
def get_game_participants(game_id: int):
    game = list_games(game_id=game_id)
    return jsonify(game_participant_schema.dump(game.participants, many=True)), 200


@api.route('/games/<int:game_id>/participants', methods=['POST'])
@swag_from(swag_path("/add_game_participants.yml"))
def add_game_participant(game_id: int):
    game = list_games(game_id=game_id)  # validate that game actually exists
    if len(game.participants) >= 2:
        current_app.logger.error(f'request to add third participant to {game}')
        raise ValidationError(message="maxiumum of 2 participants per game")
    participant = make_participant(request.json)
    return jsonify(game_participant_schema.dump(participant)), 201


@api.route('/games/<int:game_id>/scores', methods=['POST'])
@swag_from(swag_path("/add_score.yml"))
def add_score(game_id: int):
    game = update_score(game_id, request.json)
    return jsonify(game.dump(game)), 200
