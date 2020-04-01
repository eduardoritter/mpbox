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
    return render_template("plan.html", form=planForm, visits=plan.visits, patient=plan.patient, readonly=True )


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    plan = Plan.query.get(id)

    # if not plan:
    #    abort(404)

    if request.method == "GET":
        planForm = PlanForm(obj=plan)
        return render_template("plan.html", form=planForm, patient=plan.patient, readonly=False)

    form = PlanForm()
    if form.validate_on_submit():

        form.populate_obj(plan)
        db.session.add(plan)
        db.session.commit()

        flash('Record was successfully updated')
        return redirect(url_for("patient.plans", id=plan.patient_id))

    flash('Cannot update Plan')
    return render_template("plan.html", form=planForm, patient=plan.patient, readonly=False)


@bp.route("/<int:id>/delete", methods=("GET",))
def delete(id):
    plan = Plan.query.get(id)

    if not plan:
        # abort(404)
        return
    
    patient = plan.patient

    if (len( plan.visits ) > 0):
        flash('Não foi possivel excluir o plano, Existe consulta registrada!')
        return redirect(url_for("patient.plans", id=patient.id))

    db.session.delete(plan)
    db.session.commit()
    flash('Plano foi excluido!')

    return redirect(url_for("patient.plans", id=patient.id))


@bp.route("/<int:id>/visit", methods=("GET", "POST"))
def visit(id):
    plan = Plan.query.get(id)

    visit = Visit()
    visitForm = VisitForm()

    if request.method == "GET":        
        visit.date = date.today()
        visit.time = datetime.time(datetime.now())
        visitForm = VisitForm(obj=visit)
        return render_template("visit.html", form=visitForm, plano=plan)
    
    
    if visitForm.validate_on_submit():        
        visitForm.populate_obj(visit)

        for v in plan.visits:
            if v.date == visit.date:                
                flash('Já existe consulta registrada na data ' + visit.date.strftime("%d/%m/%Y"))
                return render_template("visit.html", form=visitForm, plano=plan)

        visit.plan = plan
        db.session.add(visit)
        db.session.commit()
        flash('Consulta adicionada!')
        return redirect(url_for("patient.plans", id=plan.patient_id))

    #flash('Cannot update Plan')    
    return render_template("visit.html", form=visitForm, plano=plan)


class PlanForm(FlaskForm):
    plan_type = SelectField('Plano', choices=PlanType.choices())
    payment_type = SelectField(
        'Forma de Pagamento', choices=PaymentType.choices())
    value = DecimalField('Valor', validators=[DataRequired()])
    receipt = BooleanField('Recibo')
    note = TextAreaField('Notas')
