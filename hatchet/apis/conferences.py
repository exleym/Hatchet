from flask_restplus import Namespace, Resource, fields
import logging

import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.apis.serializers import conference, team
from hatchet.util import default_list_parser


logger = logging.getLogger(__name__)
ns = Namespace("conferences", description="conference related operations")
parser = default_list_parser(namespace=ns)


@ns.route("")
class ConferenceCollection(Resource):
    @ns.doc('list conferences', parser=parser)
    @ns.marshal_with(conference)
    def get(self):
        args = parser.parse_args()
        return queries.list_resources(db.Conference)

    @ns.expect(conference)
    @ns.doc("create a new conference")
    @ns.marshal_with(conference)
    def post(self):
        conf = conference.load(ns.payload)
        return queries.persist_resource(conf, db.Conference)


@ns.route("/<int:id>", doc={"params": {"id": "conference id"}})
@ns.response(404, 'Conference not found')
class Conference(Resource):
    @ns.doc("get conference by id")
    @ns.marshal_with(conference)
    def get(self, id: int):
        return queries.get_resource(id, db.Conference)

    @ns.expect(conference)
    @ns.doc("update conference")
    @ns.marshal_with(conference)
    def put(self, id: int):
        logger.info(ns.payload)
        conf = conference.load(ns.payload)
        logger.info(conf)
        return queries.edit_resource(id, ns.payload, db.Conference)

    @ns.doc("delete conference")
    @ns.response(204, "conference deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Conference)
        return ""


@ns.route("/<int:id>/teams")
@ns.param("id", "the conference identifier")
class ConferenceTeams(Resource):
    @ns.doc("get conference teams")
    @ns.marshal_with(team)
    def get(self, id: int):
        conf = queries.get_resource(id, db.Conference)
        return conf.members
