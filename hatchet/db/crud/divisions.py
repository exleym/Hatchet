from typing import List, Union

from hatchet.extensions import db
from hatchet.errors import MissingResourceException
from hatchet.api.schemas import DivisionSchema
from hatchet.db.models import Division


division_schema = DivisionSchema()


def persist_division(division: dict) -> Division:
    division = division_schema.load(division, many=False)
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


def edit_division(division_id: int, division: dict):
    old_division = list_divisions(division_id=division_id)
    if not old_division:
        raise MissingResourceException(f'No Division with id={division_id}')
    division = division_schema.load_into(division, instance=old_division)
    db.session.add(division)
    db.session.commit()
    return division


def remove_division_by_id(division_id: int):
    division = list_divisions(division_id=division_id)
    db.session.delete(division)
    db.session.commit()
