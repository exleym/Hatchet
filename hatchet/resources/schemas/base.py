from marshmallow import fields, Schema


class BaseSchema(Schema):

    class Meta:
        unknown = "EXCLUDE"

    id = fields.Integer(allow_none=False, example=42)

