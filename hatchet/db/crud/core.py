from typing import List
from hatchet.extensions import db


ModelType = type(db.Model)


def create_resource(data: dict, model: ModelType) -> db.Model:
    obj = model(**data)
    db.session.add(obj)
    db.session.commit()
    return obj


def list_resources(model: ModelType) -> List[db.Model]:
    return model.query.all()


def get_resource(id: int, model: ModelType) -> db.Model:
    return model.query.filter_by(id=id).one()


def update_resource(id: int, data: dict, model: ModelType) -> db.Model:
    obj = get_resource(id=id, model=model)
    for k, v in data.items():
        setattr(obj, k, v)
    db.session.add(obj)
    db.session.commit()
    return obj


def remove_resource(id: int, model: ModelType) -> None:
    obj = get_resource(id=id, model=model)
    db.session.delete(obj)
    db.session.commit()
    return None