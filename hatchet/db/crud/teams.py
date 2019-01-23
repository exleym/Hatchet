from typing import List, Union

from hatchet.extensions import db
from hatchet.errors import MissingResourceException
from hatchet.api.schemas import TeamSchema
from hatchet.db.models import Team


team_schema = TeamSchema()


def persist_team(team: dict) -> Team:
    team = team_schema.load(team, many=False)
    db.session.add(team)
    db.session.commit()
    return team


def list_teams(team_id: int = None, name: str = None) -> Union[Team, List[Team]]:
    if not team_id:
        query = Team.query
        if name:
            query = query.filter_by(short_name=name)
            team = query.first()
            return team or []
        return query.all()
    team = Team.query.filter_by(id=team_id).first()
    if not team:
        raise MissingResourceException(f'No Team with id={team_id}')
    return team


def search_teams(filters: List[dict]) -> List[Team]:
    return []


def edit_team(team_id: int, team: dict):
    old_conf = list_teams(team_id=team_id)
    if not old_conf:
        raise MissingResourceException(f'No Team with id={team_id}')
    team = team_schema.load(team, instance=old_conf)
    db.session.add(team)
    db.session.commit()


def remove_team_by_id(team_id: int):
    team = list_teams(team_id=team_id)
    db.session.delete(team)
    db.session.commit()
