import logging
import marshmallow.fields as ma
from flask_restplus import Api
from flask_restplus.fields import Date, DateTime, Integer, List, Nested, String, Raw


logger = logging.getLogger(__name__)


class MarshmallowRestplusMixin(object):

    def __init__(self, *args, **kwargs):
        mm_field = kwargs.pop("mm_field")
        self.mm_field = mm_field
        super().__init__(
            *args,
            attribute=mm_field.attribute,
            required=mm_field.required,
            readonly=mm_field.load_only,
            **mm_field.metadata,
            **kwargs
        )


class RawRestplusField(MarshmallowRestplusMixin, Raw):
    pass


class StringRestplusField(MarshmallowRestplusMixin, String):
    pass


class DateRestplusField(MarshmallowRestplusMixin, Date):
    pass


class DateTimeRestplusField(MarshmallowRestplusMixin, DateTime):
    pass


class IntegerRestplusField(MarshmallowRestplusMixin, Integer):
    pass


class ListRestplusField(MarshmallowRestplusMixin, List):

    def __init__(self, *args, **kwargs):
        model = kwargs.get("mm_field")
        self.__schema_name__ = model.inner.nested.replace("Schema", "")
        nested = NestedRestplusField(mm_field=model.inner)
        super().__init__(nested, *args, **kwargs)


class NestedRestplusField(MarshmallowRestplusMixin, Nested):

    def __init__(self, *args, **kwargs):
        model = kwargs.get("mm_field")
        self.__schema_name__ = model.nested.replace("Schema", "")
        super().__init__(*args, model=model, **kwargs)



MA_TO_RP = {
    ma.Date: DateRestplusField,
    ma.String: StringRestplusField,
    ma.Integer: IntegerRestplusField,
    ma.DateTime: DateTimeRestplusField,
    ma.Nested: NestedRestplusField,
    ma.List: ListRestplusField
}


def get_restplus_field(field):
    return MA_TO_RP.get(field.__class__, StringRestplusField)


def restplus_model_from_schema(schema):
    res={}
    for fieldName, field in schema._declared_fields.items():
        RestplusClass = get_restplus_field(field)
        res[fieldName] = RestplusClass(mm_field=field)
    return res


class MarshmallowRestplusConverter(object):
    def __init__(self, api: Api = None):
        self.api = api
        self._registry = {}

    def create_model(self, schema, api: Api = None):
        api = api or self.api
        schema_name = schema.__name__.replace("Schema", "")
        _restplus_model = restplus_model_from_schema(schema)
        _restplus_model = self.enrich_nested(_restplus_model)
        model = api.model(
            schema_name,
            _restplus_model
        )
        self._registry.update({schema_name: model})
        return model

    def enrich_nested(self, model):
        for k, v in model.items():
            if isinstance(v, NestedRestplusField):
                v.model = self._registry.get(v.__schema_name__)
            elif isinstance(v, ListRestplusField):
                v.container.model = NestedRestplusField(mm_field=v.container.model)
                v.container.model = self._registry.get(v.container.model.__schema_name__)
        return model

