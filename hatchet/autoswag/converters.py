from datetime import date

TYPE_MAP = {
    int: "integer",
    str: "string",
    date: "date"
}


def pytype_to_openapi(pytype: type) -> str:
    return TYPE_MAP.get(pytype)
