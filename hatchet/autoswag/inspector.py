"""utilities for inspecting a view function and crafting an OpenAPI-compliant
YAML document that will in-turn be passed to Flasgger for serving as part of
the API documentation. This should work regardless of whether you use view
functions or the Flask-RestPLUS class/method pattern.
"""
from typing import Callable, List
import yaml

from . converters import pytype_to_openapi


class Parameter(object):
    def __init__(self, location, name, data_type):
        self.location = location
        self.name = name
        self.data_type = data_type

    def dump(self):
        return {
            "in": self.location,
            "name": self.name,
            "type": str(self.data_type)
        }


def get_path_params(f: Callable) -> List[Parameter]:
    annotations = f.__annotations__
    print(annotations)
    return [
        Parameter("path", k, pytype_to_openapi(v))
        for k, v in annotations.items()
    ]


def craft_view(f: Callable) -> str:
    view = {
        "summary": "wololo",
        "description": "a dumb, dumb thing",
        "tags": ["conferences"],
        "parameters": [],
        "responses": {"200": {"description": "a conference"}}
    }
    view["parameters"] = [x.dump() for x in get_path_params(f)]
    return yaml.dump(view)

