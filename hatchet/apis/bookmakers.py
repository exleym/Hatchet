import hatchet.db.models as db
from hatchet.apis.api_v1 import api_manager
import hatchet.resources.schemas.schemas as schemas


ns = api_manager.add_resource(
    name="bookmakers",
    resource=db.Bookmaker,
    schema=schemas.BookmakerSchema,
    description="Sports Bookmaker management resources"
)
