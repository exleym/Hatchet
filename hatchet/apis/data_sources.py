from flask_restplus import Namespace, Resource
import hatchet.db.meta_models as db
from hatchet.resources.schemas.schemas import DataSourceSchema

from hatchet.apis.api_v1 import api_manager


ns_data_sources = api_manager.add_resource(
    name="dataSources",
    resource=db.DataSource,
    schema=DataSourceSchema,
    description="External data sources"
)
