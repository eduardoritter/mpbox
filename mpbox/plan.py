from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from wtforms import SelectField, TextAreaField, BooleanField, DecimalField
from wtforms.validators import DataRequired

from mpbox import db
from mpbox.model import Patient, Plan, Visit, PaymentType, PlanType


bp = Blueprint("plan", __name__, url_prefix="/plan")


@bp.app_template_filter('to_date')
def format_datetime(date):
    return date.strftime('%d/%m/%Y')


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
    visit = Visit(plan=plan)
    db.session.add(visit)
    db.session.commit()
    flash('Consulta Adicionada.')
    return redirect(url_for("patient.index", patient_id=plan.patient_id))


class PlanForm(FlaskForm):
    plan_type = SelectField('Plano', choices=PlanType.choices())
    payment_type = SelectField(
        'Forma de Pagamento', choices=PaymentType.choices())
    value = DecimalField('Valor', validators=[DataRequired()])
    receipt = BooleanField('Recibo')
    note = TextAreaField('Notas')
