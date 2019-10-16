import logging
from typing import List, Union

from hatchet.extensions import db
from hatchet.errors import MissingResourceException
# from hatchet.resources.schemas import SurfaceSchema
from hatchet.db.models import Surface
from hatchet.db.crud.crud import CRUDManager
from hatchet.util import validate_xor


logger = logging.getLogger(__name__)
mgr = CRUDManager(Model=Surface)



def create_surface(code: str, name: str, category: str) -> Surface:
    return mgr.create(
        code=code,
        name=name,
        category=category
    )


def list_surfaces(category: str = None) -> List[Surface]:
    if category:
        return mgr.list(category=category)
    return mgr.list()


def get_surface(id: int = None, code: str = None) -> Surface:
    validate_xor(id=id, code=code)
    return mgr.get(id=id, code=code)


def edit_surface(surface_id: int, data: dict):
    surface = get_surface(id=surface_id)
    if not surface:
        raise MissingResourceException(f'No Surface with id={surface_id}')
    _ = data.pop("id", None)
    for k, v in data.items():
        setattr(surface, k, v)
    db.session.add(surface)
    db.session.commit()
    return surface


def remove_surface_by_id(surface_id: int):
    surface = list_surfaces(surface_id=surface_id)
    db.session.delete(surface)
    db.session.commit()
