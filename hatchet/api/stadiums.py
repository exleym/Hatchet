from flask import jsonify, request

from hatchet.api import api
from hatchet.extensions import db
from hatchet.errors import MissingResourceException
from hatchet.db.models import Stadium
from hatchet.api.schemas import StadiumSchema


stadium_schema = StadiumSchema()


@api.route('/stadiums', methods=['POST'])
def create_stadium():
    conf = stadium_schema.load(request.json)
    db.session.add(conf)
    db.session.commit()
    return jsonify(stadium_schema.dump(conf, many=False)), 201


@api.route('/stadiums', methods=['GET'])
def get_stadiums():
    stadiums = Stadium.query.all()
    return jsonify(stadium_schema.dump(stadiums, many=True)), 200


@api.route('/stadiums/<int:stadium_id>', methods=['GET'])
def get_stadium_by_id(stadium_id: int):
    stadium = Stadium.query.filter_by(id=stadium_id).first()
    if not stadium:
        raise MissingResourceException
    return jsonify(stadium_schema.dump(stadium, many=False)), 200
