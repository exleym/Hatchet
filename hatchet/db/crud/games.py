import logging
from typing import List, Union

logger = logging.getLogger(__name__)

from hatchet.extensions import db
from hatchet.errors import MissingResourceException
from hatchet.api.schemas import GameSchema, GameParticipantSchema
from hatchet.db.models import Game, GameParticipant, Team


game_schema = GameSchema()
participant_schema = GameParticipantSchema()


def persist_game(game: dict) -> Game:
    game = game_schema.load(game, many=False)
    db.session.add(game)
    db.session.commit()
    return game


def list_games(game_id: int = None) -> Union[Game, List[Game]]:
    if not game_id:
        return Game.query.all()
    game = Game.query.filter_by(id=game_id).first()
    if not game:
        raise MissingResourceException(f'No Game with id={game_id}')
    return game


def search_games(filters: List[dict]) -> List[Game]:
    return []


def edit_game(game_id: int, game: dict):
    old_conf = list_games(game_id=game_id)
    if not old_conf:
        raise MissingResourceException(f'No Game with id={game_id}')
    game = game_schema.load_into(game, instance=old_conf)
    db.session.add(game)
    db.session.commit()
    return game


def remove_game_by_id(game_id: int):
    game = list_games(game_id=game_id)
    db.session.delete(game)
    db.session.commit()


def make_participant(data):
    print(f"creating participant from POST data: {data}")
    participant = participant_schema.load(data)
    print(f"loaded data to participant object: {participant}")
    db.session.add(participant)
    db.session.commit()
    return participant


def get_participants(game: Game, team_id: int = None):
    query = GameParticipant.query.filter_by(game_id=game.id)
    if team_id:
        return query.filter_by(team_id=team_id).one()
    return query.all()


def update_score(game_id: int, data):
    if isinstance(data, dict):
        data = [data]
    game = list_games(game_id)
    for p in data:
        participant = get_participants(game, p.get("teamId"))
        participant.score = p.get("score")
        db.session.add(participant)
    db.session.commit()
    return game