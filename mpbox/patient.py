from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from wtforms import SelectField, TextField, StringField, TextAreaField, BooleanField, DecimalField, validators

from mpbox import db
from mpbox.model import Patient, Plan
from mpbox.plan import PlanForm, isActivePlan


bp = Blueprint("patient", __name__, url_prefix="/patient")


@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/search")
def search():
    name = request.args.get('name')    
    patients = Patient.query.filter(Patient.name.like('%' + str(name) + '%')).all()
    print(patients) 
    return render_template("index.html", patients=patients)


@bp.route("/create", methods=("GET", "POST"))
def create():
    form = PatientForm()

    if request.method == "GET":
        return render_template("patient.html", form=form)

    patient = Patient()
    form.populate_obj(patient)

    db.session.add(patient)
    db.session.commit()

    flash('Record was successfully added')

    return redirect(url_for(".index"))


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    patient = Patient.query.get(id)
    form = PatientForm(obj=patient)

    if not patient:
        abort(404)

    if request.method == "GET":
        return render_template("patient.html", form=form)

    form.populate_obj(patient)
    db.session.commit()
    flash('Record was successfully updated')

    return redirect(url_for(".index"))


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    return "Delete Patient" + str(id)


@bp.route("/<int:id>/plans", methods=("GET", "POST"))
def plans(id):
    patient = Patient.query.get(id)
    plans = patient.plans

    for p in plans:
        print(p.plan_type)

    return render_template("patient_plans.html", patient=patient, plans=plans)


@bp.route("/<int:id>/create_plan", methods=("GET", "POST"))
def create_plan(id):
    patient = Patient.query.get(id)    
    planForm = PlanForm()

    if request.method == "GET": 
        return render_template("plan.html", patient=patient, form=planForm)
    
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
        return redirect(url_for(".index"))
    
    flash('Cannot update Plan')
    return render_template("plan.html", 
                            patient=patient, plans=plans, form=planForm)


class PatientForm(FlaskForm):
    name = StringField('Nome', validators=[validators.required()])
    cpf = StringField('CPF', validators=[validators.required()])
    email = StringField('Email', validators=[validators.required(), validators.length(min=6, max=35)])
    note = TextAreaField('Notas')