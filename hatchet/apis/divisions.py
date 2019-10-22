import hatchet.db.models as db
from hatchet.resources.schemas.schemas import DivisionSchema
from hatchet.apis.api_v1 import api_manager


ns_divisions = api_manager.add_resource(
    name="divisions",
    resource=db.Division,
    schema=DivisionSchema,
    description="Conference Divisions"
)
