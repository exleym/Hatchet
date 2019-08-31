from flask import jsonify


class APIResponse(object):
    """ Handles json formatting, object serializing, etc """
    _model_schema_map = dict()

    def __init__(self):
        pass

    def register_model(self, model, schema):
        self._model_schema_map.update({model: schema})

    def error(self, error):
        if not isinstance(error, list):
            error = [error]
        errors = [str(x) for x in error]
        resp = {"errors": errors}
        return jsonify(resp)


api_response = APIResponse()
