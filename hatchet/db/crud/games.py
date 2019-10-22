import logging
from marshmallow.exceptions import ValidationError
from typing import List, Union
import sqlalchemy as sa

logger = logging.getLogger(__name__)

from hatchet.extensions import db
from hatchet.errors import MissingResourceException
from hatchet.db.models import Game, GameParticipant, Team
from sqlalchemy import asc


# def persist_game(game: dict) -> Game:
#     game = game_schema.load(game, many=False)
#     db.session.add(game)
#     db.session.commit()
#     return game


def list_games(team_id: int = None, season: int = None) -> List[Game]:
    query = Game.query
    if team_id:
        query = query.filter(Game.participants.any(team_id=team_id))
    games = query.order_by(asc(Game.game_time)).all()
    if season:
        # query = query.filter(sa.func.year(Game.game_time) == season)
        games = [g for g in games if g.game_time.year == season]
    return games



def search_games(filters: List[dict]) -> List[Game]:
    return []


def edit_game(game_id: int, game: dict, partial: bool = False):
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
    participant = participant_schema.load(data)
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


def patch_game(game_id: int, **kwargs):
    game = list_games(game_id)
    for k, v in kwargs.items():
        if not hasattr(game, k):
            raise ValidationError(f"field {k} is not a valid game attribute")
        setattr(game, k, v)
    db.session.add(game)
    db.session.commit()
    return game
