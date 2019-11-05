import logging
from marshmallow.exceptions import ValidationError
from typing import List
from hatchet.extensions import db
from hatchet.db.models import Game, GameParticipant


logger = logging.getLogger(__name__)


def list_games(team_id: int = None, season: int = None) -> List[Game]:
    query = Game.query
    if team_id:
        query = query.filter(Game.participants.any(team_id=team_id))
    games = query.all()
    if season:
        games = [g for g in games if g.game_time.year == season]
    return games


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
