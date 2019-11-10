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


@ns_weeks.route("/seasons")
class SeasonCollection(Resource):
    @ns_weeks.doc("list available seasons")
    def get(self):
        return list(set([
            x.season for x in
            models.Week.query.distinct(models.Week.season).all()
        ]))