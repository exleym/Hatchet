from flask import jsonify, request

from hatchet.api import api
from hatchet.api.schemas.schemas import StadiumSchema
from hatchet.extensions import swag
import hatchet.db.crud.stadiums as query


stadium_swagger_path = "../static/swagger/stadiums"
swagger_view = swag.get_view(stadium_swagger_path)
schema = StadiumSchema()


@api.route("/stadiums", methods=["POST"])
@swagger_view
def create_stadium():
    stadium = query.persist_stadium(request.json)
    return jsonify(schema.dump(stadium, many=False)), 200


@api.route("/stadiums", methods=["GET"])
@swagger_view
def get_stadiums():
    stadiums = query.list_stadiums()
    return jsonify(schema.dump(stadiums, many=True)), 200


@api.route("/stadiums/<int:stadium_id>", methods=["GET"])
@swagger_view
def get_stadium_by_id(stadium_id: int):
    stadium = query.list_stadiums(stadium_id=stadium_id)
    return jsonify(schema.dump(stadium, many=False)), 200


@api.route("/stadiums/<int:stadium_id>", methods=["PUT"])
@swagger_view
def update_stadium(stadium_id: int):
    stadium = query.edit_stadium(stadium_id=stadium_id, stadium=request.json)
    return jsonify(schema.dump(stadium, many=False)), 200

@api.route("/stadiums/<int:stadium_id>", methods=["DELETE"])
@swagger_view
def delete_stadium(stadium_id: int):
    query.remove_stadium_by_id(stadium_id=stadium_id)
    return jsonify(""), 204
