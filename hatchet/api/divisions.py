from flask import jsonify, request

from hatchet.api import api
from hatchet.extensions import db
from hatchet.errors import MissingResourceException
from hatchet.db.models import Division
from hatchet.api.schemas import DivisionSchema, TeamSchema


division_schema = DivisionSchema()
team_schema = TeamSchema()


@api.route('/divisions', methods=['POST'])
def create_division():
    division = division_schema.load(request.json)
    db.session.add(division)
    db.session.commit()
    return jsonify(division_schema.dump(division, many=False)), 201


@api.route('/divisions', methods=['GET'])
def get_divisions():
    query = apply_division_filters(request.args)
    divisions = query.all()
    return jsonify(division_schema.dump(divisions, many=True)), 200


@api.route('/divisions/<int:division_id>', methods=['GET'])
def get_division_by_id(division_id: int):
    division = Division.query.filter_by(id=division_id).first()
    if not division:
        msg = f'No Division with id={division_id}'
        raise MissingResourceException(message=msg, status_code=404)
    return jsonify(division_schema.dump(division, many=False)), 200


@api.route('/divisions/<int:division_id>', methods=['PUT'])
def update_division(division_id: int):
    division = Division.query.filter_by(id=division_id).first()
    if not division:
        raise MissingResourceException
    division = division_schema.load(request.json, instance=division)
    db.session.add(division)
    db.session.commit()
    return jsonify(division_schema.dump(division, many=False), 200)


@api.route('/divisions/<int:division_id>', methods=['DELETE'])
def delete_division(division_id: int):
    division = Division.query.filter_by(id=division_id).first()
    if not division:
        msg = f'No Division with id={division_id}'
        raise MissingResourceException(message=msg)
    db.session.delete(division)
    db.session.commit()
    return jsonify(""), 204


@api.route('/divisions/<int:division_id>/members', methods=['GET'])
def get_division_members(division_id: int):
    division = Division.query.filter_by(id=division_id).first()
    if not division:
        raise MissingResourceException
    return jsonify(team_schema.dump(division.members, many=True)), 200


@api.route('/divisions/<int:division_id>/standings', methods=['GET'])
def get_division_standings(division_id: int):
    division = Division.query.get(division_id)
    return jsonify(team_schema.dump(division.standings, many=True)), 200


def apply_division_filters(args):
    query = Division.query
    conf_id = args.get("conferenceId")
    if conf_id:
        query = query.filter(Division.conference_id==conf_id)
    return query
