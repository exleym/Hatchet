from flask_restplus import Resource
import hatchet.db.models as models
from hatchet.apis.api_v1 import api_manager
from hatchet.apis.serializers import ranking
import hatchet.resources.schemas.schemas as schemas
from hatchet.errors import InvalidArgumentError


ns_polls = api_manager.add_resource(
    name="polls",
    resource=models.Poll,
    schema=schemas.PollSchema,
    description="NCAA Football Polls / Rankings"
)


@ns_polls.route("/<int:id>/rankings/season/<int:season>/week/<int:week>")
@ns_polls.param("id", "the poll identifier")
@ns_polls.param("season", "season")
@ns_polls.param("week", "week")
class ExternalTeamLookup(Resource):
    @ns_polls.doc("lookup rankings for a specific poll and week")
    @ns_polls.marshal_with(ranking)
    def get(self, id:int, season:int, week:int):
        wk = models.Week.query.filter_by(season=season, number=week).first()
        if not wk:
            raise InvalidArgumentError(
                f"you passed an invalid season {season} or week {week}"
            )
        return models.Ranking.query\
            .filter_by(poll_id=id)\
            .filter_by(week_id=wk.id)\
            .order_by(models.Ranking.rank)\
            .all()


@ns_polls.route("/<int:id>/rankings/week/<int:week_id>")
@ns_polls.param("id", "the poll identifier")
@ns_polls.param("week_id", "week id (not the week of the season)")
class ExternalTeamWeeklyLookup(Resource):
    @ns_polls.doc("lookup rankings for a specific poll by week")
    @ns_polls.marshal_with(ranking)
    def get(self, id:int,  week_id:int):
        wk = models.Week.query.filter_by(id=week_id).first()
        if not wk:
            raise InvalidArgumentError(
                f"you passed an invalid week_id={week_id}"
            )
        return models.Ranking.query\
            .filter_by(poll_id=id)\
            .filter_by(week_id=wk.id)\
            .order_by(models.Ranking.rank)\
            .all()