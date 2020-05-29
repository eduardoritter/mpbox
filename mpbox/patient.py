from datetime import date
from dateutil.relativedelta import relativedelta

from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from flask_login import login_required
from wtforms import SelectField, TextField, StringField, TextAreaField, BooleanField, DecimalField, DateField, validators
from sqlalchemy.sql import exists

from mpbox.extensions import db
from mpbox.model import Patient, Visit, Plan, AdditionalPaymentType
from mpbox.plan import PlanForm
from mpbox.validators import is_active_plan, has_active_plan, validate_plan, validate_patient, ValidationError
from mpbox.config import BASE_URL_PREFIX


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
          
        db.session.add(patient)
        db.session.commit()

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


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    return 'Delete Patient' + str(id)


@bp.route('/<int:id>/plans', methods=('GET', 'POST'))
@login_required
def plans(id):
    
    patient = Patient.query.get(id)
    plans = patient.plans

    activePlans = []
    oldPlans =[]

    for p in plans:
        if is_active_plan(p):
            activePlans.append(p)
        else:
            oldPlans.append(p)

    return render_template('patient_plans.html', patient=patient, 
                            activePlans=activePlans, oldPlans=oldPlans)


@bp.route('/<int:id>/create_plan', methods=('GET', 'POST'))
@login_required
def create_plan(id):
    patient = Patient.query.get(id)
    expiry = date.today() + relativedelta(months=6)
    planForm = PlanForm(additional_value=0.00, paid=True, 
                        expiry_date=date.today() + relativedelta(months=6))

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


class PatientForm(FlaskForm):
    name = StringField('Nome', validators=[validators.required()])
    cpf = StringField('CPF', validators=[validators.required()])
    email = StringField('Email', validators=[validators.Email(), validators.required()])
    birthdate = DateField('Data de Nascimento', format='%d/%m/%Y', validators=[validators.required()])
    note = TextAreaField('Notas')