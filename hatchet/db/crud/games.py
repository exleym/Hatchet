import datetime as dt
import logging
from marshmallow.exceptions import ValidationError
from typing import List
from hatchet.extensions import db
import hatchet.db.models as models
from hatchet.util.validators import validate_xor


logger = logging.getLogger(__name__)


def list_games(team_id: int = None, season: int = None, date: dt.date = None) -> List[models.Game]:
    logger.warning(f"queries games with season={season} and date={date}")
    query = models.Game.query
    if team_id:
        query = query.filter(models.Game.participants.any(team_id=team_id))
    if season or date:
        validate_xor(season=season, date=date)
        if season:
            season = models.Season.query.filter_by(id=season).one()
            end_date = season.end_date + dt.timedelta(days=1)
            date = season.start_date
        else:
            end_date = date + dt.timedelta(days=1)
        query = query.filter(models.Game.game_time <= end_date)
        query = query.filter(models.Game.game_time >= date)
    query = query.order_by(models.Game.game_time)
    return query.all()


def list_week_games(week_id: int) -> List[models.Game]:
    week = models.Week.query.filter_by(id=week_id).one()
    end_date = week.end_date + dt.timedelta(days=1)
    return models.Game.query\
        .filter(models.Game.game_time > week.start_date)\
        .filter(models.Game.game_time < end_date)\
        .all()


def get_team_record_by_season(team_id: int, season: int):
    games = list_games(team_id=team_id, season=season)
    record = _craft_record(team_id=team_id, games=games)
    record.update({"season": season})
    return record


def get_participants(game: models.Game, team_id: int = None):
    query = models.GameParticipant.query.filter_by(game_id=game.id)
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


def _craft_record(team_id: int, games: List[models.Game]) -> dict:
    wins = [g for g in games if g.winner and g.winner.team_id == team_id]
    losses = [g for g in games if g.winner and g.winner.team_id != team_id]
    conf_wins = [
        g for g in wins
        if g.winner.team.conference_id == g.loser.team.conference_id
    ]
    conf_losses = [
        g for g in losses
        if g.winner.team.conference_id == g.loser.team.conference_id
    ]
    return {
        "wins": len(wins),
        "losses": len(losses),
        "confWins": len(conf_wins),
        "confLosses": len(conf_losses)
    }