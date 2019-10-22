import hatchet.db.models as db
from hatchet.apis.api_v1 import api_manager
import hatchet.resources.schemas.schemas as schemas


ns_coaches = api_manager.add_resource(
    name="coaches",
    resource=db.Coach,
    schema=schemas.CoachSchema,
    description="NCAA Football Coaches"
)
