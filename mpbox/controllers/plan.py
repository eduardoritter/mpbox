from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_login import login_required

from mpbox.config import BASE_URL_PREFIX
from mpbox.services import plans, visits
from .forms import PlanForm, VisitForm


bp = Blueprint('plan', __name__, url_prefix=BASE_URL_PREFIX + 'plan')


@bp.app_template_filter('to_date')
def format_date(date):
    return date.strftime('%d/%m/%Y')


@bp.app_template_filter('to_time')
def format_time(time):
    return time.strftime('%H:%M')


@bp.app_template_filter('to_visit_sequence')
def visit_sequence(sequence):
    if sequence == 1:
        return 'Primeira'
    if sequence == 2:
        return 'Segunda'
    if sequence == 3:
        return 'Terceira'
    if sequence == 4:
        return 'Quarta'
    return sequence


@bp.route('/<int:id>')
@login_required
def display(id):
    plan = plans.get(id)
    form = PlanForm(obj=plan)
    return render_template('plan.html', form=form, visits=plan.visits, patient=plan.patient, readonly=True)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    plan = plans.get(id)
    form = PlanForm(obj=plan)

    if form.validate_on_submit():
        form.populate_obj(plan)

        try:
            plans.save(plan)
        except Exception as error:
            flash(error)
        else:
            flash('Plano foi atualizado com sucesso!')
            return redirect(url_for('patient.my_plans', id=plan.patient_id))

    return render_template('plan.html', form=form, patient=plan.patient, readonly=False)


@bp.route('/<int:id>/delete', methods=('GET',))
@login_required
def delete(id):
    plan = plans.get(id)
    patient_id = plan.patient_id

    try:
        plans.delete(plan)
        flash('Plano foi excluido com sucesso!')
    except Exception as error:
        flash(str(error))
        
    return redirect(url_for('patient.my_plans', id=patient_id))


@bp.route('/<int:id>/visit', methods=('GET', 'POST'))
def visit(id):
    plan = plans.get(id)
    form = VisitForm()

    if form.validate_on_submit():
        visit = visits.new_and_populate(form)
        visit.plan = plan
        
        try:
            #????
            visits.save(visit)
        except Exception as error:
            flash(error)
        else:
            flash('Consulta registrada com sucesso!')
            return redirect(url_for('patient.plans', id=plan.patient_id))

    if not form.is_submitted():
        form = VisitForm(obj=visits.new_set_default(plan=plan))
    
    return render_template('visit.html', form=form, plan=plan)
