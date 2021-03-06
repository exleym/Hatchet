import hatchet.db.models as db
from hatchet.apis.api_v1 import api_manager
import hatchet.resources.schemas.schemas as schemas


ns = api_manager.add_resource(
    name="stadiums",
    resource=db.Stadium,
    schema=schemas.StadiumSchema,
    description="Football Stadium operations"
)