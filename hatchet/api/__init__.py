from flask import Blueprint, jsonify


api = Blueprint('api', __name__)


@api.route('/status')
def status():
    status_package = {"status": "ok"}
    return jsonify(status_package)


from hatchet.api.conferences import *
from hatchet.api.divisions import *
from hatchet.api.stadiums import *
from hatchet.api.teams import *
