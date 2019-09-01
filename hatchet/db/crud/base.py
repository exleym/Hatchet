import logging
from typing import List

from hatchet.extensions import db
from hatchet.errors import throw_mre

logger = logging.getLogger(__name__)


def persist_resource(data: dict, model_class: type(db.Model)) -> db.Model:
    obj = model_class(**data)
    db.session.add(obj)
    db.session.commit()
    return obj


def list_resources(model_class: type(db.Model)) -> List[db.Model]:
    return model_class.query.all()


def get_resource(id: int, model_class: type(db.Model)) -> db.Model:
    obj = model_class.filter_by(id=id).first()
    if not obj:
        logger.error(f"error looking up {model_class.__name__} with id={id}")
        throw_mre(id, model_class)
    return obj


def search(filters: List[dict], model_class: type(db.Model)) -> List[db.Model]:
    return []


def edit_resource(id: int, data: dict, model_class: type(db.Model)) -> db.Model:
    obj = get_resource(id=id, model_class=model_class)
    _ = data.pop("id", None)
    for k, v in data.items():
        setattr(obj, k, v)
    db.session.add(obj)
    db.session.commit()
    return obj


def remove_resource_by_id(id: int, model_class: type(db.Model)):
    obj = get_resource(id=id, model_class=model_class)
    db.session.delete(obj)
    db.session.commit()
