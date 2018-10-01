from marshmallow import Schema, fields


class ErrorSchema(Schema):
    type = fields.String(attribute='error_type')
    message = fields.String()


class ApplicationException(Exception):
    error_type = None
    message = None
    status_code = 200


class MissingResourceException(ApplicationException):
    error_type = None
    message = 'The resource you requested cannot be found'
    status_code = 404
