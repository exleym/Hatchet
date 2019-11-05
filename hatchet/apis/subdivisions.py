from flask_restplus import Resource
import logging
import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.resources.schemas.schemas import ConferenceSchema, SubdivisionSchema, TeamSchema
from hatchet.apis.api_v1 import api_manager
from hatchet.apis.serializers import conference, team


logger = logging.getLogger(__name__)
ns_subdivisions = api_manager.add_resource(
    name="subdivisions",
    resource=db.Subdivision,
    schema=SubdivisionSchema,
    description="NCAA Subdivisions"
)


@ns_subdivisions.route("/<int:id>/conferences")
@ns_subdivisions.param("id", "the subdivision identifier")
class SubdivisionConferences(Resource):
    @ns_subdivisions.doc("get subdivision conferences")
    @ns_subdivisions.marshal_with(conference)
    def get(self, id: int):
        subdiv = queries.get_resource(id, db.Subdivision)
        return subdiv.conferences


@ns_subdivisions.route("/<int:id>/teams")
@ns_subdivisions.param("id", "the subdivision identifier")
class SubdivisionTeams(Resource):
    @ns_subdivisions.doc("get teams beloning to a subdivision")
    @ns_subdivisions.marshal_with(team)
    def get(self, id: int):
        subdiv = queries.get_resource(id, db.Subdivision)
        return subdiv.teams