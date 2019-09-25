import logging
from typing import List
from hatchet.extensions import db
from hatchet.errors import MissingResourceException


logger = logging.getLogger(__name__)
ModelType = type(db.Model)


def persist_resource(data: dict, model: ModelType) -> db.Model:
    obj = model(**data)
    db.session.add(obj)
    db.session.commit()
    return obj


def list_resources(model: ModelType) -> List[db.Model]:
    return model.query.all()


def get_resource(id: int, model: ModelType) -> db.Model:
    obj = model.query.filter_by(id=id).first()
    if not obj:
        logger.error(f"error looking up {model.__name__} with id={id}")
        msg = f"No {model.__name__} with id={id}"
        raise MissingResourceException(msg)
    return obj


def search(filters: List[dict], model: ModelType) -> List[db.Model]:
    return []


def edit_resource(id: int, data: dict, model: ModelType) -> db.Model:
    obj = get_resource(id=id, model=model)
    _ = data.pop("id", None)
    for k, v in data.items():
        setattr(obj, k, v)
    db.session.add(obj)
    db.session.commit()
    return obj


def remove_resource_by_id(id: int, model: ModelType):
    obj = get_resource(id=id, model=model)
    db.session.delete(obj)
    db.session.commit()
