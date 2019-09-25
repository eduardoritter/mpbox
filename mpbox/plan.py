from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from wtforms import SelectField, TextAreaField, BooleanField, DecimalField, validators

from mpbox import db
from mpbox.model import Patient, Plan, Visit, PaymentType, PlanType


bp = Blueprint("plan", __name__, url_prefix="/plan")


def isActivePlan(plan):
    if (plan.plan_type == PlanType.P2 and
       len(plan.visits) < 2):
        return True

    if (plan.plan_type == PlanType.P4 and
       len(plan.visits) < 4):
        return True

    return False

@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    plan = Plan.query.get(id)
    planForm = PlanForm(obj=plan)

    if not plan:
        abort(404)

    if request.method == "GET":
        return render_template("plan.html", form=planForm)

    plan = populatePlan(plan, request)                                
    
    db.session.add(plan)
    db.session.commit()

    flash('Record was successfully updated')

    return redirect(url_for("patient.index"))


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    return "Delete Plan" + str(id)


@bp.route("/<int:id>/visit", methods=("GET", "POST"))
def visit(id):
    plan = Plan.query.get(id)
    visit = Visit(plan=plan)
    db.session.add(visit)
    db.session.commit()
    flash('Consulta Adicionada.')
    return redirect(url_for("patient.index", patient_id=plan.patient_id))


def populatePlan(plan, request, *patient):

    plan.plan_type=request.form.get("plan_type")
    plan.payment_type=request.form.get("payment_type")
    plan.value=request.form.get("value")
    plan.receipt=request.form.get("receipt")
    plan.note=request.form.get("note")

    if patient is None:
        plan.patient=patient

    return plan


class PlanForm(FlaskForm):
    plan_type = SelectField('Plano', 
                            choices=PlanType.choices(),
                            coerce=PlanType.coerce)
    payment_type = SelectField('Forma de Pagamento', 
                               choices=PaymentType.choices(), 
                               coerce=PaymentType.coerce)
    value = DecimalField('Valor', validators=[validators.required()])
    receipt = BooleanField('Recibo')
    note = TextAreaField('Notas')