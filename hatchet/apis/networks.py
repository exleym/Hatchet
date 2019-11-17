import hatchet.db.models as db
from hatchet.apis.api_v1 import api_manager
import hatchet.resources.schemas.schemas as schemas


ns_networks = api_manager.add_resource(
    name="networks",
    resource=db.Network,
    schema=schemas.NetworkSchema,
    description="Media Networks"
)
