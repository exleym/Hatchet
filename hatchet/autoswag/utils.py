def get_schemas(spec):
    if spec.openapi_version.major < 3:
        return spec.to_dict()["definitions"]
    return spec.to_dict()["components"]["schemas"]