from apispec.ext.marshmallow.swagger import schema2jsonschema
from flasgger import Swagger, swag_from


class AutoSwag(Swagger):
    """Extends the Flasgger Swagger extension to support OpenAPI inference

    Use this class to write less Swagger doc yourself. You can register
    a schema to the OpenAPI spec using the ``@schema`` decorator, which
    if you are using the "NameSchema" convention, will register the
    inferred definition as "Name".


    """
    def schema(self, obj):
        name = obj.__name__.replace("Schema", "")
        if not self.config.get("definitions"):
            self.config["definitions"] = {}
        spec = schema2jsonschema(obj)
        self.config.get("definitions").update({name: spec})
        return obj

    def view(self, path, filename=None):
        def decorator(f):
            swagger_file = filename or f"{f.__name__}.yml"
            swagger_path = f"{path}/{swagger_file}"
            swag_from(swagger_path)(f)
            return f
        return decorator

    def get_view(self, path):
        return self.view(path)

    def autoswag(self, f):
        return f