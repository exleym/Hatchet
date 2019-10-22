import hatchet.db.models as db
from hatchet.apis.api_v1 import api_manager
import hatchet.resources.schemas.schemas as schemas


ns = api_manager.add_resource(
    name="players",
    resource=db.Player,
    schema=schemas.PlayerSchema,
    description="Football Player management endpoints"
)
