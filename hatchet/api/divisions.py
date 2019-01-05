from flask import jsonify, request

from hatchet.api import api, api_response
from hatchet.db.crud.divisions import (
    edit_division,
    list_divisions,
    persist_division,
    remove_division_by_id
)


@api.route('/divisions', methods=['POST'])
def create_division():
    division = persist_division(request.json)
    return api_response.dump(division, 201)


@api.route('/divisions', methods=['GET'])
def get_divisions():
    divisions = list_divisions()
    return api_response.dump(divisions, 200)


@api.route('/divisions/<int:division_id>', methods=['GET'])
def get_division_by_id(division_id: int):
    division = list_divisions(division_id=division_id)
    return api_response.dump(division, 200)


@api.route('/divisions/<int:division_id>/members', methods=['GET'])
def get_division_members(division_id: int):
    division = list_divisions(division_id=division_id)
    return api_response.dump(division.members, 200)


@api.route('/divisions/<int:division_id>', methods=['PUT'])
def update_division(division_id: int):
    conf = edit_division(division_id=division_id, division=request.json)
    return api_response.dump(conf, 200)


@api.route('/divisions/<int:division_id>', methods=['DELETE'])
def delete_division(division_id: int):
    remove_division_by_id(division_id=division_id)
    return jsonify(""), 204
