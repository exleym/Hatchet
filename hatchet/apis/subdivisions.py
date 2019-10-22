from flask_restplus import Resource
import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.resources.schemas.schemas import ConferenceSchema, SubdivisionSchema, TeamSchema
from hatchet.apis.api_v1 import api_manager


ns_subdivisions = api_manager.add_resource(
    name="subdivisions",
    resource=db.Subdivision,
    schema=SubdivisionSchema,
    description="NCAA Subdivisions"
)
conference = api_manager.model(ConferenceSchema)
team = api_manager.model(TeamSchema)


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