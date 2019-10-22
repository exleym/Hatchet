from flask_restplus import Api, Namespace
import flask_sqlalchemy as db
from marshmallow import Schema


class Cruddite(object):
    def __init__(self, namespace: Namespace, resource: type(db.Model),
                 schema: type(Schema), description: str = None):
        self.ns = namespace
        self.resource = resource
        self.schema = schema
        self.description = description

