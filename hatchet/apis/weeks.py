from flask_restplus import Resource
import hatchet.db.models as models
from hatchet.apis.api_v1 import api_manager
from hatchet.apis.serializers import ranking
import hatchet.resources.schemas.schemas as schemas
from hatchet.errors import InvalidArgumentError


ns_weeks = api_manager.add_resource(
    name="weeks",
    resource=models.Week,
    schema=schemas.WeekSchema,
    description="NCAA Football Weeks / Rankings",
    parser_args=["season"]
)
