from flask_restplus import Namespace, Resource, fields
import logging

import hatchet.db.models as db
import hatchet.db.crud.base as queries
from hatchet.apis.serializers import subdivision, conference, team
from hatchet.util import default_list_parser


logger = logging.getLogger(__name__)
ns = Namespace("subdivisions", description="subdivision related operations")
parser = default_list_parser(namespace=ns)
parser.add_argument(
    "code",
    type=str,
    required=False,
    help="fetch subdivision matching code",
    location="args"
)


@ns.route("")
class SubdivisionCollection(Resource):
    @ns.doc('list subdivisions', parser=parser)
    @ns.marshal_with(subdivision)
    def get(self):
        args = parser.parse_args()
        logger.warning(args)
        return queries.list_resources(db.Subdivision, code=args.get("code"))

    @ns.expect(subdivision, validate=True)
    @ns.doc("create a new subdivision")
    @ns.marshal_with(subdivision)
    def post(self):
        conf = ns.payload
        return queries.persist_resource(conf, db.Subdivision)


@ns.route("/<int:id>")
@ns.response(404, 'Subdivision not found')
@ns.param('id', 'The subdivision identifier')
class Subdivision(Resource):
    @ns.doc("get subdivision by id")
    @ns.marshal_with(subdivision)
    def get(self, id: int):
        return queries.get_resource(id, db.Subdivision)

    @ns.expect(subdivision, validate=True)
    @ns.doc("update subdivision")
    @ns.marshal_with(subdivision)
    def put(self, id: int):
        return queries.edit_resource(id, ns.payload, db.Subdivision)

    @ns.doc("delete subdivision")
    @ns.response(204, "subdivision deleted")
    def delete(self, id: int):
        queries.remove_resource_by_id(id, db.Subdivision)
        return ""


@ns.route("/<int:id>/conferences")
@ns.param("id", "the subdivision identifier")
class SubdivisionConferences(Resource):
    @ns.doc("get subdivision conferences")
    @ns.marshal_with(conference)
    def get(self, id: int):
        subdiv = queries.get_resource(id, db.Subdivision)
        return subdiv.conferences


@ns.route("/<int:id>/teams")
@ns.param("id", "the subdivision identifier")
class SubdivisionTeams(Resource):
    @ns.doc("get teams beloning to a subdivision")
    @ns.marshal_with(team)
    def get(self, id: int):
        subdiv = queries.get_resource(id, db.Subdivision)
        return subdiv.teams