from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm, Form
from wtforms import SelectField, TextField, StringField, TextAreaField, BooleanField, DecimalField, validators

from mpbox import db
from mpbox.model import Patient


bp = Blueprint("patient", __name__, url_prefix="/patient")


@bp.route("/")
def index():
    return "All Patient"


@bp.route("/create", methods=("GET", "POST"))
def create():
    form = PatientForm()

    if request.method == "GET":
        return render_template("patient.html", form=form)

    patient = Patient()
    form.populate_obj(patient)

    db.session.add(patient)
    db.session.commit()

    return render_template("patient.html", form=form)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    return "Update Patient" + str(id)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    return "Delete Patient" + str(id)


@bp.route("/<int:id>/plans", methods=("GET", "POST"))
def plans(id):
    return "Plans" + str(id)


@bp.route("/<int:id>/create_plan", methods=("GET", "POST"))
def create_plan(id):
    return "Create plan" + str(id)


class PatientForm(FlaskForm):
    name = StringField('Nome', validators=[validators.required()])
    cpf = StringField('CPF', validators=[validators.required()])
    email = StringField('Email', validators=[validators.required(), validators.length(min=6, max=35)])
    note = TextAreaField('Notas')