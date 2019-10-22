from typing import List
from hatchet.extensions import db


def persist_resource(Model: type(db.Model), **kwargs) -> db.Model:
    resource = Model(**kwargs)
    db.session.add(resource)
    db.session.commit()
    return resource


def list_resources(Model: type(db.Model), **kwargs) -> List[db.Model]:
    query = Model.query
    for k, v in kwargs.items():
        query = query.filter_by(k=v)
    return query.all()


def get_resource(Model: type(db.Model), id: int = None, code: str = None) -> db.Model:
    if id:
        return Model.query.filter_by(id=id).one()
    return Model.query.filter_by(code=code).one()


def delete_resource(Model: type(db.Model), id: int) -> None:
    resource = get_resource(Model=Model, id=id)
    db.session.delete(resource)
    db.session.commit()
    return None


class CRUDManager(object):
    def __init__(self, Model: type(db.Model)):
        self.Model = Model

    def create(self, **kwargs):
        return persist_resource(Model=self.Model, **kwargs)

    def list(self, **kwargs):
        return list_resources(Model=self.Model, **kwargs)

    def get(self, id: int = None, code: str = None) -> db.Model:
        return get_resource(Model=self.Model, id=id, code=code)

    def delete(self, id: int) -> None:
        return delete_resource(Model=self.Model, id=id)