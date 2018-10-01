from flask import Blueprint, jsonify


api = Blueprint('api', __name__)


@api.route('/status')
def status():
    status_package = {"status": "ok"}
    return jsonify(status_package)