from marshmallow import Schema, fields


class ErrorSchema(Schema):
    message = fields.String(attribute='messages')


class ApplicationException(Exception):
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        if not isinstance(message, dict) and not isinstance(message, list):
            messages = [message]
        else:
            messages = message
        self.messages = messages
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
