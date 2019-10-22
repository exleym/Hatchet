from flask_restplus import Resource
import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.resources.schemas.schemas import ConferenceSchema

from hatchet.apis.api_v1 import api_manager



ns_conferences = api_manager.add_resource(
    name="conferences",
    resource=db.Conference,
    schema=ConferenceSchema,
    description="NCAA Football Conferences"
)


@ns_conferences.route("/<int:id>/teams")
@ns_conferences.param("id", "the conference identifier")
class ConferenceTeams(Resource):
    @ns_conferences.doc("get conference teams")
    @ns_conferences.marshal_with(team)
    def get(self, id: int):
        conf = queries.get_resource(id, db.Conference)
        return conf.members
