from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form

from mpbox import db
from mpbox.model import Visit


bp = Blueprint("visit", __name__, url_prefix="/visit")


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    visit = Visit.query.get(id)

    if not visit:
       #abort(404)
       return

    plan=visit.plan

    db.session.delete(visit)
    db.session.commit()

    return redirect(url_for("plan.display", id=plan.id))  


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    return "Delete Visit" + str(id)
