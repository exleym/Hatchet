from flask import jsonify, request

from hatchet.resources import api
from hatchet.extensions import swag
import hatchet.db.crud.divisions as query
from hatchet.resources.schemas.schemas import (
    DivisionSchema,
    TeamSchema,
)

div_schema = DivisionSchema()
team_schema = TeamSchema()


division_swagger_path = "../static/swagger/divisions"
swagger_view = swag.get_view(division_swagger_path)


@api.route('/divisions', methods=['POST'])
@swagger_view
def create_division():
    division = query.persist_division(request.json)
    return jsonify(div_schema.dump(division)), 201


@api.route('/divisions', methods=['GET'])
@swagger_view
def get_divisions():
    divisions = query.list_divisions()
    return jsonify(div_schema.dump(divisions, many=True)), 200


@api.route('/divisions/<int:division_id>', methods=['GET'])
@swagger_view
def get_division_by_id(division_id: int):
    division = query.list_divisions(division_id=division_id)
    return jsonify(div_schema.dump(division)), 200


@api.route('/divisions/<int:division_id>/members', methods=['GET'])
@swagger_view
def get_division_members(division_id: int):
    division = query.list_divisions(division_id=division_id)
    return jsonify(team_schema.dump(division.members)), 200


@api.route('/divisions/<int:division_id>', methods=['PUT'])
@swagger_view
def update_division(division_id: int):
    division = query.edit_division(division_id=division_id, division=request.json)
    return jsonify(div_schema.dump(division)), 200


@api.route('/divisions/<int:division_id>', methods=['DELETE'])
@swagger_view
def delete_division(division_id: int):
    query.remove_division_by_id(division_id=division_id)
    return jsonify(""), 204
