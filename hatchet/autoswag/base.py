from apispec.ext.marshmallow.swagger import schema2jsonschema
from flasgger import Swagger


class AutoSwag(Swagger):
    def schema(self, obj):
        name = obj.__name__.replace("Schema", "")
        if not self.config.get("definitions"):
            self.config["definitions"] = {}
        spec = schema2jsonschema(obj)
        self.config.get("definitions").update({name: spec})
        return obj
