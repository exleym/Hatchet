from flask import jsonify, request

from hatchet.api import api
from hatchet.extensions import db
from hatchet.errors import MalformedRequestException, MissingResourceException
from hatchet.db.models import Conference
from hatchet.api.schemas import ConferenceSchema, DivisionSchema, TeamSchema


conference_schema = ConferenceSchema()
team_schema = TeamSchema()
division_schema = DivisionSchema()


@api.route('/conferences', methods=['POST'])
def create_conference():
    print(request.json)
    conf = conference_schema.load(request.json, many=False)
    print(conf)
    print(type(conf))
    db.session.add(conf)
    db.session.commit()
    return jsonify(conference_schema.dump(conf, many=False)), 201


@api.route('/conferences', methods=['GET'])
def get_conferences():
    conferences = Conference.query.all()
    return jsonify(conference_schema.dump(conferences, many=True)), 200


@api.route('/conferences/<int:conference_id>', methods=['GET'])
def get_conference_by_id(conference_id: int):
    conference = Conference.query.filter_by(id=conference_id).first()
    if not conference:
        raise MissingResourceException
    return jsonify(conference_schema.dump(conference, many=False)), 200


@api.route('/conferences/<int:conference_id>/divisions', methods=['GET'])
def get_conference_divisions(conference_id: int):
    conference = Conference.query.filter_by(id=conference_id).first()
    if not conference:
        raise MissingResourceException
    return jsonify(division_schema.dump(conference.divisions, many=True)), 200


@api.route('/conferences/<int:conference_id>/members', methods=['GET'])
def get_conference_members(conference_id: int):
    conference = Conference.query.filter_by(id=conference_id).first()
    if not conference:
        raise MissingResourceException
    return jsonify(team_schema.dump(conference.members, many=True)), 200


@api.route('/conferences/<int:conference_id>', methods=['PUT'])
def update_conference(conference_id: int):
    conference = Conference.query.filter_by(id=conference_id).first()
    if not conference:
        raise MissingResourceException
    conference = conference_schema.load(request.json, instance=conference)
    db.session.add(conference)
    db.session.commit()
    return jsonify(conference_schema.dump(conference, many=False), 200)


@api.route('/conferences/<int:conference_id>', methods=['DELETE'])
def delete_conference(conference_id: int):
    conference = Conference.query.filter_by(id=conference_id).first()
    if not conference:
        raise MissingResourceException
    db.session.delete(conference)
    db.session.commit()
    return jsonify(""), 204