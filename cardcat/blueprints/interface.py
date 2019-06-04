from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from cardcat.models import Log
from datetime import datetime
from cardcat.database import db

bp = Blueprint("interface", __name__)


@bp.route("/log", methods=["POST", "GET"])
def log():
    json = request.json
    foo = Log()
    foo.amount = json.get("amount")
    foo.dttm = datetime.fromisoformat(json.get("dt"))
    foo.vendor = json.get("vendor")
    foo.card = json.get("card")
    foo.token = json.get("token")
    db.session.add(foo)
    db.session.commit()
    return jsonify(message="logged")


@bp.route("/view/<token>", methods=['post', 'get'])
def categorize(token):
    if request.method == 'POST':
        charge = Log.query.filter_by(token=token).first_or_404()
        charge.person = request.form["person"]
        charge.category = request.form["category"]
        db.session.commit()
        return redirect(url_for('interface.home'))
    charge = Log.query.filter_by(token=token).first_or_404()

    return render_template("charge.html", charge=charge)


@bp.route("/solobolo")
def home():
    charges = Log.query.order_by(Log.dttm.desc()).all()
    return render_template("summary.html", charges=charges)
