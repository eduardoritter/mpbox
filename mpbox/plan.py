from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from wtforms import SelectField, TextAreaField, BooleanField, DecimalField
from wtforms.validators import DataRequired

from mpbox import db
from mpbox.model import Patient, Plan, Visit, PaymentType, PlanType
from mpbox.visit import VisitForm

from datetime import date, time, datetime


bp = Blueprint("plan", __name__, url_prefix="/plan")


@bp.app_template_filter('to_date')
def format_date(date):
    return date.strftime("%d/%m/%Y")


@bp.app_template_filter('to_time')
def format_date(time):
    return time.strftime("%H:%M")


def isActivePlan(plan):
    if (plan.plan_type == PlanType.P2 and
            len(plan.visits) < 2):
        return True

    if (plan.plan_type == PlanType.P4 and
            len(plan.visits) < 4):
        return True

    return False


@bp.route("/<int:id>")
def display(id):
    plan = Plan.query.get(id)
    planForm = PlanForm(obj=plan)
    return render_template("plan.html", form=planForm, visits=plan.visits, readonly=True)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    plan = Plan.query.get(id)

    # if not plan:
    #    abort(404)

    if request.method == "GET":
        planForm = PlanForm(obj=plan)
        return render_template("plan.html", form=planForm)

    form = PlanForm()
    if form.validate_on_submit():

        form.populate_obj(plan)
        db.session.add(plan)
        db.session.commit()

        flash('Record was successfully updated')
        return redirect(url_for("patient.plans", id=plan.patient_id))

    flash('Cannot update Plan')
    return render_template("plan.html", form=planForm)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    return "Delete Plan" + str(id)


@bp.route("/<int:id>/visit", methods=("GET", "POST"))
def visit(id):
    plan = Plan.query.get(id)

    visit = Visit()

    if request.method == "GET":        
        visit.date = date.today()
        visit.time = datetime.time(datetime.now())
        visitForm = VisitForm(obj=visit)
        return render_template("visit.html", form=visitForm, plano=plan)

    form = VisitForm()
    if form.validate_on_submit():
        form.populate_obj(visit)
        visit.plan = plan
        db.session.add(visit)
        db.session.commit()
        flash('Visita adicionada.')
        return redirect(url_for("patient.plans", id=plan.patient_id))

    #flash('Cannot update Plan')
    return render_template("visit.html", form=form, plano=plan)

        

    


class PlanForm(FlaskForm):
    plan_type = SelectField('Plano', choices=PlanType.choices())
    payment_type = SelectField(
        'Forma de Pagamento', choices=PaymentType.choices())
    value = DecimalField('Valor', validators=[DataRequired()])
    receipt = BooleanField('Recibo')
    note = TextAreaField('Notas')
