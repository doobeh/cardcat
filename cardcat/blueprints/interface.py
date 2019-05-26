from flask import Blueprint, jsonify


bp = Blueprint("interface", __name__)


@bp.route('/log', methods=['post', 'get'])
def log():
    return jsonify(message='logged')