from marshmallow import Schema, fields


class ErrorSchema(Schema):
    message = fields.String()



class ApplicationException(Exception):
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload


class MalformedRequestException(ApplicationException):
    def __init__(self, message=None, status_code=400, payload=None):
        message = message or "malformed request body"
        super().__init__(message, status_code, payload)


class MissingResourceException(ApplicationException):
    def __init__(self, message=None, status_code=404, payload=None):
        message = message or "the resource you requested cannot be found"
        super().__init__(message, status_code, payload)
