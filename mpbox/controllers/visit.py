from flask import Blueprint, render_template, redirect, request, url_for, flash

from mpbox.services import visits
from mpbox.utils import ValidationError
from mpbox.config import BASE_URL_PREFIX
from .forms import VisitForm


bp = Blueprint('visit', __name__, url_prefix=BASE_URL_PREFIX + 'visit')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    visit = visits.get(id)
    form = VisitForm(obj=visit)

    if form.validate_on_submit():
        form.populate_obj(visit)

        try:
            visits.save(visit)
        except ValidationError as error:
            flash(error)
        else:
            flash('Consulta foi atualizada com sucesso!')
            return redirect(url_for('patient.plans', id=visit.plan.patient_id))

    return render_template('visit.html', form=form, plan=visit.plan)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    visit = visits.get(id)
    plan = visit.plan

    try:
        visits.delete(visit)
        flash('Consulta foi excluída com sucesso!')
    except Exception as error:
        flash(str(error))

    return redirect(url_for('plan.display', id=plan.id))
