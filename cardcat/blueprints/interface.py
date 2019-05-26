from flask import Blueprint, jsonify, request
from cardcat.models import Log
from datetime import datetime
from cardcat.database import db

bp = Blueprint("interface", __name__)


@bp.route('/log', methods=['POST', 'GET'])
def log():
    json = request.json
    foo = Log()
    foo.amount = json.get('amount')
    foo.dttm = datetime.fromisoformat(json.get('dt'))
    foo.vendor = json.get('vendor')
    foo.card = json.get('card')
    db.session.add(foo)
    db.session.commit()
    return jsonify(message='logged')