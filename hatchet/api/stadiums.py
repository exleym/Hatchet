from flask import jsonify, request

from hatchet.api import api, api_response
from hatchet.db.crud.stadiums import (
    edit_stadium,
    list_stadiums,
    persist_stadium,
    remove_stadium_by_id
)


@api.route('/stadiums', methods=['POST'])
def create_stadium():
    stadium = persist_stadium(request.json)
    return api_response.dump(stadium, 201)


@api.route('/stadiums', methods=['GET'])
def get_stadiums():
    stadiums = list_stadiums()
    return api_response.dump(stadiums, 200)


@api.route('/stadiums/<int:stadium_id>', methods=['GET'])
def get_stadium_by_id(stadium_id: int):
    stadium = list_stadiums(stadium_id=stadium_id)
    return api_response.dump(stadium, 200)


@api.route('/stadiums/<int:stadium_id>', methods=['PUT'])
def update_stadium(stadium_id: int):
    conf = edit_stadium(stadium_id=stadium_id, stadium=request.json)
    return api_response.dump(conf, 200)


@api.route('/stadiums/<int:stadium_id>', methods=['DELETE'])
def delete_stadium(stadium_id: int):
    remove_stadium_by_id(stadium_id=stadium_id)
    return jsonify(""), 204
