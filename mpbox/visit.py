from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from wtforms import DateField, TimeField
from wtforms.validators import DataRequired

from mpbox import db
from mpbox.model import Visit


bp = Blueprint("visit", __name__, url_prefix="/visit")


@bp.app_template_filter('to_date')
def format_date(date):
    return date.strftime('%d/%m/%Y')


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):

    visit = Visit.query.get(id)

    if not visit:
        # abort(404)
        return

    if request.method == "GET":
        visitForm = VisitForm(obj=visit)
        return render_template("visit.html", form=visitForm)

    form = VisitForm()
    if form.validate_on_submit():
        form.populate_obj(visit)
        db.session.add(visit)
        db.session.commit()

        flash('Record was successfully updated')
        return redirect(url_for("patient.plans", id=visit.plan.patient_id))

    return "Delete Visit" + str(id)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    visit = Visit.query.get(id)

    if not visit:
        # abort(404)
        return

    plan = visit.plan

    db.session.delete(visit)
    db.session.commit()

    return redirect(url_for("plan.display", id=plan.id))


class VisitForm(FlaskForm):
    date = DateField('Data', format='%d/%m/%Y', validators=[DataRequired()])
    time = TimeField('Hora', validators=[DataRequired()])
