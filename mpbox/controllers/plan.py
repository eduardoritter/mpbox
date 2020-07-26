from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_login import login_required

from mpbox.utils import validate_plan, validate_new_visit, ValidationError
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
    planForm = PlanForm(obj=plan)
    return render_template('plan.html', form=planForm, visits=plan.visits, patient=plan.patient, readonly=True)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    plan = plans.get(id)
    planForm = PlanForm(obj=plan)

    if request.method == 'GET':
        return render_template('plan.html', form=planForm, patient=plan.patient, readonly=False)

    if planForm.validate_on_submit():

        planForm.populate_obj(plan)

        try:
            validate_plan(plan)
        except Exception as error:
            flash(error)
            return render_template('plan.html', form=planForm, patient=plan.patient, readonly=False)

        plans.save(plan)

        flash('Plano foi atualizado com sucesso!')
        return redirect(url_for('patient.plans', id=plan.patient_id))

    flash('Erro não foi possível atualizar o plano!')
    return render_template('plan.html', form=planForm, patient=plan.patient, readonly=False)


@bp.route('/<int:id>/delete', methods=('GET',))
@login_required
def delete(id):
    plan=plans.get(id)
    patient=plan.patient

    try:
        plans.delete(plan)
        flash('Plano foi excluido com sucesso!')
    except Exception as error:
        flash(str(error))
        return redirect(url_for('patient.plans', id=patient.id))
        
    return redirect(url_for('patient.plans', id=patient.id))


@bp.route('/<int:id>/visit', methods=('GET', 'POST'))
def visit(id):
    plan = plans.get(id)

    visit = visits.new()
    visitForm = VisitForm()

    if request.method == 'GET':

        visit.sequence_number = len(plan.visits) + 1
        visitForm = VisitForm(obj=visit)
        return render_template('visit.html', form=visitForm, plan=plan)
        
    if visitForm.validate_on_submit():        
        visitForm.populate_obj(visit)
        
        try:
            validate_new_visit(visit, plan)
        except Exception as error:
            flash(error)
            return render_template('visit.html', form=visitForm, plan=plan)

        visit.plan = plan

        visits.save(visit)
        
        flash('Consulta registrada com sucesso!')
        return redirect(url_for('patient.plans', id=plan.patient_id))

    flash('Erro não foi possível registrar consulta!')   
    return render_template('visit.html', form=visitForm, plan=plan)


@bp.route('json/<int:id>')
def display_json(id):
    
    if request.is_json:
        return request.get_json()
    
    return 'OI'

