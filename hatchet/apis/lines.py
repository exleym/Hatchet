import hatchet.db.models as db
from hatchet.apis.api_v1 import api_manager
import hatchet.resources.schemas.schemas as schemas


ns = api_manager.add_resource(
    name="lines",
    resource=db.Line,
    schema=schemas.LineSchema,
    description="Sports Gambling lines",
    parser_args=["game_id", "team_id"]
)
