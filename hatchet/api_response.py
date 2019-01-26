from typing import Any, List, Union
from flask import jsonify

from hatchet.errors import ErrorSchema


class ApiResponse(object):

    def __init__(self):
        self.error_schema = ErrorSchema()

    def dump(self, data: Union[List[Any], Any] = None,
             errors: Union[List[Exception], Exception] = None):
        pkg = dict()
        if data:
            pkg.update({"data": data})
        if errors:
            many = isinstance(errors, list)
            pkg.update({"errors": self.error_schema.dump(errors, many=many)})
        return jsonify(pkg)
