from flask import jsonify, request

from hatchet.api import api
from hatchet.extensions import db
from hatchet.errors import MissingResourceException
from hatchet.db.models import Team
from hatchet.api.schemas import TeamSchema


team_schema = TeamSchema()


@api.route('/teams', methods=['POST'])
def create_team():
    conf = team_schema.load(request.json)
    db.session.add(conf)
    db.session.commit()
    return jsonify(team_schema.dump(conf, many=False)), 201


@api.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify(team_schema.dump(teams, many=True)), 200


@api.route('/teams/<int:team_id>', methods=['GET'])
def get_team_by_id(team_id: int):
    team = Team.query.filter_by(id=team_id).first()
    if not team:
        raise MissingResourceException
    return jsonify(team_schema.dump(team, many=False)), 200
