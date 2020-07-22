from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form

from mpbox.services import plans, visits
from mpbox.extensions import db
from mpbox.utils import validate_visit, ValidationError
from mpbox.config import BASE_URL_PREFIX
from .forms import VisitForm


bp = Blueprint('visit', __name__, url_prefix=BASE_URL_PREFIX + 'visit')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):

    visit = visits.get(id)

    if not visit:
        flash('Internal Error')
        return redirect(url_for('home.home'))

    visitForm = VisitForm(obj=visit)

    if request.method == 'GET':        
        return render_template('visit.html', form=visitForm, plan=visit.plan)
       
    if visitForm.validate_on_submit():
        visitForm.populate_obj(visit)

        try:
            validate_visit(visit)
        except ValidationError as error:
            flash(error)
            return render_template('visit.html', form=visitForm, plan=visit.plan)

        visits.save(visit)

        flash('Consulta foi atualizada com sucesso!')
        return redirect(url_for('patient.plans', id=visit.plan.patient_id))

    flash('Erro não foi possível atualizar a consulta!')
    return render_template('visit.html', form=visitForm, plan=visit.plan)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    visit = visits.get(id)

    if not visit:
        flash('Internal Error')
        return redirect(url_for('home.home'))

    plan = visit.plan

    visits.delete(visit)

    flash('Consulta foi excluída com sucesso!')
    return redirect(url_for('plan.display', id=plan.id))