import hatchet.db.models as db
from hatchet.apis.api_v1 import api_manager
import hatchet.resources.schemas.schemas as schemas


ns_ratings = api_manager.add_resource(
    name="ratings",
    resource=db.Rating,
    schema=schemas.RatingSchema,
    description="TV Ratings"
)

