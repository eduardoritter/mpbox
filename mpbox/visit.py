from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from wtforms import DateField, TimeField, SelectField
from wtforms.validators import DataRequired

from mpbox.extensions import db
from mpbox.model import Visit, PlanType


bp = Blueprint("visit", __name__)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):

    visit = Visit.query.get(id)

    if not visit:
        # abort(404)
        return

    if request.method == "GET":
        visitForm = VisitForm(obj=visit)
        return render_template("visit.html", form=visitForm, plano=visit.plan)

    form = VisitForm()
    
    if form.validate_on_submit():
        form.populate_obj(visit)
        db.session.add(visit)
        db.session.commit()

        flash('Consulta foi atualizada com sucesso!')
        return redirect(url_for("patient.plans", id=visit.plan.patient_id))

    flash('Erro não foi possível atualizar a consulta!')
    return render_template("visit.html", form=form, plano=visit.plan)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    visit = Visit.query.get(id)

    if not visit:
        # abort(404)
        return

    plan = visit.plan

    db.session.delete(visit)
    db.session.commit()
    flash('Consulta foi excluída com sucesso!')
    return redirect(url_for("plan.display", id=plan.id))


class VisitForm(FlaskForm):
    sequence_number = SelectField('Consulta', choices=[(1, 'Primeira'), (2, 'Segunda'), (3, 'Terceira'), (4, 'Quarta')], coerce=int)
    date = DateField('Data', format='%d/%m/%Y', validators=[DataRequired()])
    time = TimeField('Hora', validators=[DataRequired()])
