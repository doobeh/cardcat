from flask import Blueprint, jsonify


bp = Blueprint("interface", __name__)


@bp.route('/log', methods=['POST', 'GET'])
def log():
    return jsonify(message='logged')