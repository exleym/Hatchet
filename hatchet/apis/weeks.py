from flask_restplus import Resource
from sqlalchemy import desc
import hatchet.db.models as models
from hatchet.apis.api_v1 import api_manager
from hatchet.apis.serializers import ranking, game
from hatchet.db.crud.games import list_week_games
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
        return [
            x.id for x in
            models.Season.query.order_by(desc(models.Season.id)).all()
        ]


@ns_weeks.route("/<int:id>/games")
@ns_weeks.param("id", "week identifier for game filtering")
class WeeklyGameCollection(Resource):
    @ns_weeks.marshal_with(game)
    def get(self, id: int):
        return list_week_games(week_id=id)


