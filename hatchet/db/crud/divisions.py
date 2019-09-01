from typing import List, Union

from hatchet.extensions import db
from hatchet.errors import MissingResourceException
from hatchet.db.models import Division



def persist_division(division: dict) -> Division:
    division = Division(**division)
    db.session.add(division)
    db.session.commit()
    return division


def list_divisions(division_id: int = None) -> Union[Division,
                                                     List[Division]]:
    if not division_id:
        return Division.query.all()
    division = Division.query.filter_by(id=division_id).first()
    if not division:
        raise MissingResourceException(f'No Division with id={division_id}')
    return division


def search_divisions(filters: List[dict]) -> List[Division]:
    return []


def edit_division(division_id: int, data: dict):
    division = list_divisions(division_id=division_id)
    if not division:
        raise MissingResourceException(f'No Division with id={division_id}')
    _ = data.pop("id", None)
    for k, v in data.items():
        setattr(division, k, v)
    db.session.add(division)
    db.session.commit()
    return division


def remove_division_by_id(division_id: int):
    division = list_divisions(division_id=division_id)
    db.session.delete(division)
    db.session.commit()
