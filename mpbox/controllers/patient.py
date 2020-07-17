from datetime import date
from dateutil.relativedelta import relativedelta

from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from flask_login import login_required

from sqlalchemy.sql import exists

from mpbox.extensions import db
from mpbox.models import Patient, Visit, Plan, AdditionalPaymentType
from mpbox.utils import validate_plan, validate_patient, ValidationError, classify_plans, is_active_plan, has_active_plan
from mpbox.config import BASE_URL_PREFIX
from .forms import PatientForm, PlanForm
from ..services import PatientService


bp = Blueprint('patient', __name__, url_prefix=BASE_URL_PREFIX + 'patient')


def patient_exist(patient):
    if db.session.query(exists().where(Patient.cpf == patient.cpf)).scalar():
        raise ValidationError('Paciente ' + patient.name + ' já registrado!')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PatientForm()

    if request.method == 'GET':
        return render_template('patient.html', form=form)

    if form.validate_on_submit():

        patient = Patient()        
        form.populate_obj(patient)

        try:
            validate_patient(patient)
            patient_exist(patient)
        except ValidationError as error:
            flash(error)
            return render_template('patient.html', form=form)

        patient_service = PatientService()
        patient_service.save(patient)

        flash('Paciente foi adicionado !')
        return redirect(url_for('patient.plans', id=patient.id))
        
    return render_template('patient.html', form=form)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    patient = Patient.query.get(id)
    form = PatientForm(obj=patient)

    if request.method == 'GET':
        return render_template('patient.html', form=form)

    if form.validate_on_submit():

        form.populate_obj(patient)

        try:
            validate_patient(patient)
        except Exception as error:
            flash(error)
            return render_template('patient.html', form=form) 

        db.session.add(patient)
        db.session.commit()

        flash('Paciente foi atualizado !')
        return redirect(url_for('home.home'))

    return render_template('patient.html', form=form)


@bp.route('/<int:id>/delete', methods=('GET',))
@login_required
def delete(id):
    patient = Patient.query.get(id)

    if (len( patient.plans ) > 0):
        flash('Não foi possivel excluir o paciente, Existe plano vinculado ao paciente!')
        return redirect(url_for('home.home'))
    
    db.session.delete(patient)
    db.session.commit()
    flash('Paciente foi excluido com sucesso!')
    return redirect(url_for('home.home'))


@bp.route('/<int:id>/plans', methods=('GET', 'POST'))
@login_required
def plans(id):
    
    patient = Patient.query.get(id)
    active_plans, old_plans = classify_plans(patient.plans)

    return render_template('patient_plans.html', patient=patient, 
                            activePlans=active_plans, oldPlans=old_plans)


@bp.route('/<int:id>/create_plan', methods=('GET', 'POST'))
@login_required
def create_plan(id):
    patient = Patient.query.get(id)
    expiry = date.today() + relativedelta(months=6)
    planForm = PlanForm(additional_value=0.00, paid=True, expiry_date=expiry)

    if request.method == 'GET': 
        return render_template('plan.html', patient=patient, 
                               form=planForm, readonly=False)
    
    plans = patient.plans

    if has_active_plan(plans):
        flash(patient.name + ' já possui plano ativo!')        
        return render_template('plan.html', patient=patient, plans=plans, 
                               form=planForm, readonly=False)
   
    if planForm.validate_on_submit():
        plan = Plan()
        planForm.populate_obj(plan)

        try:
            validate_plan(plan)
        except Exception as error:
            flash(error)            
            return render_template('plan.html', patient=patient, plans=plans, 
                                   form=planForm, readonly=False)

        plan.patient=patient                               
    
        db.session.add(plan)
        db.session.commit()

        flash('Plano foi cadastrado com sucesso!')
        return redirect(url_for('patient.plans', id=patient.id))
    
    flash('Erro: Plano não cadastrado!')
    return render_template('plan.html', patient=patient, plans=plans, 
                           form=planForm, readonly=False)
