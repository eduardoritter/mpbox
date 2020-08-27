from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required

from mpbox.utils import ValidationError, classify_plans, has_active_plan
from mpbox.config import BASE_URL_PREFIX
from .forms import PatientForm, PlanForm
from mpbox.services import patients, plans

bp = Blueprint('patient', __name__, url_prefix=BASE_URL_PREFIX + 'patient')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PatientForm()

    if form.validate_on_submit():
        patient = patients.new_and_populate(form)

        try:
            patients.create(patient)
        except ValidationError as error:
            flash(error)
        else:
            flash('Paciente foi adicionado!')
            return redirect(url_for('patient.plans', id=patient.id))

    return render_template('patient.html', form=form)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    patient = patients.get_or_404(id)
    form = PatientForm(obj=patient)

    if form.validate_on_submit():
        form.populate_obj(patient)
        try:
            patients.save(patient)
        except Exception as error:
            flash(error)
        else:
            flash('Paciente %s foi atualizado!' % patient.name)
            return redirect(url_for('home.home'))

    return render_template('patient.html', form=form)


@bp.route('/<int:id>/delete', methods=('GET',))
@login_required
def delete(id):
    patient = patients.get(id)

    try:
        patients.delete(patient)
        flash('Paciente %s foi excluido com sucesso!' % patient.name)
    except Exception as error:
        flash(str(error))

    return redirect(url_for('home.home'))


@bp.route('/<int:id>/plans', methods=('GET', 'POST'))
@login_required
def my_plans(id):
    patient = patients.get(id)
    active_plans, old_plans = classify_plans(patient.plans)

    return render_template('patient_plans.html', patient=patient, activePlans=active_plans, oldPlans=old_plans)


@bp.route('/<int:id>/create_plan', methods=('GET', 'POST'))
@login_required
def create_plan(id):
    patient = patients.get(id)
    form = PlanForm()

    if form.validate_on_submit():
        plan = plans.new_and_populate(form)
        plan.patient = patient
        try:
            plans.save(plan)
        except Exception as error:
            flash(error)
        else:
            flash('Plano foi cadastrado com sucesso!')
            return redirect(url_for('patient.my_plans', id=patient.id))

    if not form.is_submitted():
        if has_active_plan(patient.plans):
            flash('Paciente %s já possui um plano ativo!' % patient.name)
            return redirect(url_for('patient.my_plans', id=patient.id))

        form = PlanForm(obj=plans.new_set_default())

    return render_template('plan.html', patient=patient, form=form, readonly=False)
