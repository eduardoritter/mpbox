from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from wtforms import DateField, TimeField, SelectField
from wtforms.validators import DataRequired

from mpbox.extensions import db
from mpbox.model import Visit, PlanType
from mpbox.validators import validate_visit
from mpbox.config import BASE_URL_PREFIX


bp = Blueprint('visit', __name__, url_prefix=BASE_URL_PREFIX + 'visit')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):

    visit = Visit.query.get(id)

    if not visit:
        flash('Internal Error')
        return redirect(url_for('home.home'))

    visitForm = VisitForm(obj=visit)

    if request.method == 'GET':        
        return render_template('visit.html', form=visitForm, plano=visit.plan)
       
    if visitForm.validate_on_submit():
        visitForm.populate_obj(visit)

        try:
            validate_visit(visit, None)
        except Exception as error:
            flash(error)
            return render_template('visit.html', form=visitForm, plano=visit.plan)

        db.session.add(visit)
        db.session.commit()

        flash('Consulta foi atualizada com sucesso!')
        return redirect(url_for('patient.plans', id=visit.plan.patient_id))

    flash('Erro não foi possível atualizar a consulta!')
    return render_template('visit.html', form=visitForm, plano=visit.plan)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    visit = Visit.query.get(id)

    if not visit:
        flash('Internal Error')
        return redirect(url_for('home.home'))

    plan = visit.plan

    db.session.delete(visit)
    db.session.commit()
    flash('Consulta foi excluída com sucesso!')
    return redirect(url_for('plan.display', id=plan.id))


class VisitForm(FlaskForm):
    sequence_number = SelectField('Consulta', choices=[(1, 'Primeira'), (2, 'Segunda'), (3, 'Terceira'), (4, 'Quarta')], coerce=int)
    date = DateField('Data', format='%d/%m/%Y', validators=[DataRequired()])
    time = TimeField('Hora', validators=[DataRequired()])
