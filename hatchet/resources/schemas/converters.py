import logging
import marshmallow.fields as ma
from flask_restplus.fields import Date, DateTime, Integer, List, Nested, String, Raw


logger = logging.getLogger(__name__)


class MarshmallowRestplusMixin(object):

    def __init__(self, *args, **kwargs):
        mm_field = kwargs.pop("mm_field")
        self.mm_field = mm_field
        logger.warning(mm_field)
        print(mm_field.metadata)
        print(mm_field.__dict__)
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
    pass


class NestedRestplusField(MarshmallowRestplusMixin, Nested):
    pass


MA_TO_RP = {
    ma.Date: DateRestplusField,
    ma.Integer: IntegerRestplusField,
    ma.DateTime: DateTimeRestplusField,
    ma.Nested: NestedRestplusField,
    ma.List: ListRestplusField
}


def get_restplus_field(field):
    return MA_TO_RP.get(field.__class__, RawRestplusField)


def restplus_model_from_schema(schema):
    logger.warning(f"getting restplus model from schema {schema}")
    res={}
    for fieldName, field in schema._declared_fields.items():
        RestplusClass = get_restplus_field(field)
        logger.warning(f"got class {RestplusClass}")
        res[fieldName] = RestplusClass(mm_field=field)
    return res
