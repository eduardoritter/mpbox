from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from wtforms import SelectField, TextField, StringField, TextAreaField, BooleanField, DecimalField, DateField, validators
from flask_login import login_required, current_user

from mpbox import db
from mpbox.model import Patient, Visit, Plan
from mpbox.plan import PlanForm, isActivePlan


bp = Blueprint("patient", __name__, url_prefix="/patient")


@login_required
@bp.route("/")
def index():
    lastVisits = Visit.query.order_by(Visit.created.desc()).limit(5)    
    return render_template("index.html", lastVisits=lastVisits)


@login_required
@bp.route("/search")
def search():
    name = request.args.get('name')    
    patients = Patient.query.filter(Patient.name.like('%' + str(name) + '%')).all()

    return render_template("index.html", patients=patients)

@login_required
@bp.route("/create", methods=("GET", "POST"))
def create():
    form = PatientForm()

    if request.method == "GET":
        return render_template("patient.html", form=form)

    patient = Patient()

    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.add(patient)
        db.session.commit()

        flash('Paciente foi adicionado !')
        return redirect(url_for(".index"))

    return render_template("patient.html", form=form)


@login_required
@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    patient = Patient.query.get(id)
    form = PatientForm(obj=patient)

    if request.method == "GET":
        return render_template("patient.html", form=form)

    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.add(patient)
        db.session.commit()

        flash('Paciente foi atualizado !')
        return redirect(url_for(".index"))

    return render_template("patient.html", form=form)


@login_required
@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    return "Delete Patient" + str(id)


@login_required
@bp.route("/<int:id>/plans", methods=("GET", "POST"))
def plans(id):
    patient = Patient.query.get(id)
    plans = patient.plans

    activePlans = []
    oldPlans =[]

    for p in plans:
        if isActivePlan(p):
            activePlans.append(p)
        else:
            oldPlans.append(p)

    return render_template("patient_plans.html", patient=patient, activePlans=activePlans, oldPlans=oldPlans)


@login_required
@bp.route("/<int:id>/create_plan", methods=("GET", "POST"))
def create_plan(id):
    patient = Patient.query.get(id)    
    planForm = PlanForm(additional_value=0.00)

    if request.method == "GET": 
        return render_template("plan.html", patient=patient, form=planForm, readonly=False)
    
    plans = patient.plans
    for plan in plans:
        if isActivePlan(plan):
            flash('Existe plano ativo!')
            return render_template("plan.html",
                                   patient=patient, plans=plans, form=planForm)
   
    if planForm.validate_on_submit():
        plan = Plan()
        planForm.populate_obj(plan)
        plan.patient=patient                               
    
        db.session.add(plan)
        db.session.commit()

        flash('Record was successfully added')
        return redirect(url_for("patient.plans", id=patient.id))
    
    flash('Cannot update Plan')
    return render_template("plan.html", 
                            patient=patient, plans=plans, form=planForm)


class PatientForm(FlaskForm):
    name = StringField('Nome', validators=[validators.required()])
    cpf = StringField('CPF', validators=[validators.required()])
    email = StringField('Email', validators=[validators.Email(), validators.required()])
    birthdate = DateField('Data de Nascimento', format='%d/%m/%Y', validators=[validators.required()])
    note = TextAreaField('Notas')