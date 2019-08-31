from flask import jsonify, request
from flasgger import swag_from

from hatchet.resources import api
from hatchet.resources.schemas.schemas import (
    ConferenceSchema,
    DivisionSchema,
    TeamSchema
)
from hatchet.db.crud.conferences import (
    edit_conference,
    list_conferences,
    persist_conference,
    remove_conference_by_id
)


conf_schema = ConferenceSchema()
div_schema = DivisionSchema()
team_schema = TeamSchema()


def swag_path(context):
    SWAGGER_PATH = "../static/swagger/conferences"
    return SWAGGER_PATH + context


@api.route('/conferences', methods=['POST'])
@swag_from(swag_path('/create_conference.yml'))
def create_conference():
    conference = persist_conference(request.json)
    return jsonify(conf_schema.dump(conference)), 201


@api.route('/conferences', methods=['GET'])
@swag_from(swag_path("/get_conferences.yml"))
def get_conferences():
    conferences = list_conferences()
    return jsonify(conf_schema.dump(conferences, many=True)), 200


@api.route('/conferences/<int:conference_id>', methods=['GET'])
@swag_from(swag_path('/get_conference_by_id.yml'))
def get_conference_by_id(conference_id: int):
    conference = list_conferences(conference_id=conference_id)
    return jsonify(conf_schema.dump(conference)), 200


@api.route('/conferences/<int:conference_id>/divisions', methods=['GET'])
@swag_from(swag_path("/get_conference_divisions.yml"))
def get_conference_divisions(conference_id: int):
    conference = list_conferences(conference_id=conference_id)
    return jsonify(div_schema.dump(conference.divisions, many=True)), 200


@api.route('/conferences/<int:conference_id>/members', methods=['GET'])
@swag_from(swag_path("/get_conference_members.yml"))
def get_conference_members(conference_id: int):
    conference = list_conferences(conference_id=conference_id)
    return jsonify(team_schema.dump(conference.members, many=True)), 200


@api.route('/conferences/<int:conference_id>', methods=['PUT'])
@swag_from(swag_path("/update_conference.yml"))
def update_conference(conference_id: int):
    request.json.pop("id", None)
    conf = edit_conference(conference_id=conference_id, conference=request.json)
    return jsonify(conf_schema.dump(conf)), 200


@api.route('/conferences/<int:conference_id>', methods=['DELETE'])
@swag_from(swag_path("/delete_conference.yml"))
def delete_conference(conference_id: int):
    remove_conference_by_id(conference_id=conference_id)
    return jsonify(""), 204
