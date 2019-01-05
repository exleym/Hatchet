from flask import jsonify

from hatchet.errors import ApplicationException
from hatchet.api.schemas import REGISTERED_SCHEMAS


class APIResponse(object):
    """ Handles json formatting, object serializing, etc """
    _model_schema_map = dict()

    def __init__(self, model_map: dict):
        self._model_schema_map.update(model_map)

    def register_model(self, model, schema):
        self._model_schema_map.update({model: schema})

    def dump(self, data, code):
        dump_many = False
        if isinstance(data, list):
            dump_many = True
            if not data:
                return jsonify([], many=True), code
            data_type = type(data[0])
        else:
            data_type = type(data)
        Schema = self._model_schema_map.get(data_type)
        if not Schema:
            raise ApplicationException('A serializer is unregistered')
        schema = Schema()
        return jsonify(schema.dump(data, many=dump_many)), code


# This is the Singleton APIResponse object that should be used throughout
# the application.
api_response = APIResponse(
    {schema._Model: schema for schema in REGISTERED_SCHEMAS}
)