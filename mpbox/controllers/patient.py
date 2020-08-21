from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from flask_login import login_required

from mpbox.extensions import db
from mpbox.utils import ValidationError, classify_plans, is_active_plan, has_active_plan
from mpbox.config import BASE_URL_PREFIX
from .forms import PatientForm, PlanForm
from mpbox.services import patients, plans


bp = Blueprint('patient', __name__, url_prefix=BASE_URL_PREFIX + 'patient')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PatientForm()

    if request.method == 'GET':
        return render_template('patient.html', form=form)

    if form.validate_on_submit():

        patient = patients.new_and_populate(form)       

        try:
            patients.create(patient)
        except ValidationError as error:
            flash(error)
        else:
            flash('Paciente foi adicionado !')
            return redirect(url_for('patient.plans', id=patient.id))

    else:
        flash('Erro não foi possível cadastrar o paciente!')
        
    return render_template('patient.html', form=form)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    patient = patients.get_or_404(id)
    
    form = PatientForm(obj=patient)

    if request.method == 'GET':
        return render_template('patient.html', form=form)

    if form.validate_on_submit():

        form.populate_obj(patient)

        try:
            patients.save(patient)
        except Exception as error:
            flash(error)
        else:
            flash('Paciente %s foi atualizado!' % patient.name)
            return redirect(url_for('home.home'))
    
    else:
        flash('Erro não foi possível atualizar o paciente!')
    
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

    return render_template('patient_plans.html', patient=patient, 
                            activePlans=active_plans, oldPlans=old_plans)


@bp.route('/<int:id>/create_plan', methods=('GET', 'POST'))
@login_required
def create_plan(id):
    patient = patients.get(id)

    if request.method == 'GET':
        if has_active_plan(patient.plans):
            flash('Paciente %s já possui um plano ativo!' % patient.name)        
            return redirect(url_for('patient.my_plans', id=patient.id))
        
        form = PlanForm(plans.new_set_default())
        return render_template('plan.html', patient=patient, 
                               form=form, readonly=False)
    
    form = PlanForm(request.form)

    if form.validate_on_submit():
        plan = plans.new()
        form.populate_obj(plan)

        try:
            plan.patient=patient 
            plans.save(plan)  
        except Exception as error:
            flash(error)            
        else:
            flash('Plano foi cadastrado com sucesso!')
            return redirect(url_for('patient.my_plans', id=patient.id))
    
    else:
        flash('Erro: Plano não cadastrado!')
    
    return render_template('plan.html', patient=patient,
                           form=form, readonly=False)
