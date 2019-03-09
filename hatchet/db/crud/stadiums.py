from typing import List, Union

from hatchet.extensions import db
from hatchet.errors import MissingResourceException
from hatchet.api.schemas import StadiumSchema
from hatchet.db.models import Stadium


stadium_schema = StadiumSchema()


def persist_stadium(stadium: dict) -> Stadium:
    stadium = stadium_schema.load(stadium, many=False)
    db.session.add(stadium)
    db.session.commit()
    return stadium


def list_stadiums(stadium_id: int = None) -> Union[Stadium,
                                                         List[Stadium]]:
    if not stadium_id:
        return Stadium.query.all()
    stadium = Stadium.query.filter_by(id=stadium_id).first()
    if not stadium:
        raise MissingResourceException(f'No Stadium with id={stadium_id}')
    return stadium


def search_stadiums(filters: List[dict]) -> List[Stadium]:
    return []


def edit_stadium(stadium_id: int, stadium: dict):
    old_conf = list_stadiums(stadium_id=stadium_id)
    if not old_conf:
        raise MissingResourceException(f'No Stadium with id={stadium_id}')
    stadium = stadium_schema.load_into(stadium, instance=old_conf)
    db.session.add(stadium)
    db.session.commit()
    return stadium


def remove_stadium_by_id(stadium_id: int):
    stadium = list_stadiums(stadium_id=stadium_id)
    db.session.delete(stadium)
    db.session.commit()
