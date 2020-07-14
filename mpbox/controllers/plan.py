from datetime import datetime
import pytz

from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_wtf import FlaskForm, Form
from flask_login import login_required
from wtforms import SelectField, TextAreaField, BooleanField, DecimalField, DateField
from wtforms.validators import DataRequired

from mpbox.extensions import db
from mpbox.models import Patient, Plan, Visit, PaymentType, PlanType, AdditionalPaymentType
from .visit import VisitForm
from mpbox.utils import validate_plan, validate_new_visit, ValidationError 
from mpbox.config import BASE_URL_PREFIX


bp = Blueprint('plan', __name__, url_prefix=BASE_URL_PREFIX + 'plan')


@bp.app_template_filter('to_date')
def format_date(date):
    return date.strftime('%d/%m/%Y')


@bp.app_template_filter('to_time')
def format_time(time):
    return time.strftime('%H:%M')


@bp.app_template_filter('to_visit_sequence')
def visit_sequence(sequence):
    if sequence == 1:
        return 'Primeira'
    if sequence == 2:
        return 'Segunda'
    if sequence == 3:
        return 'Terceira'
    if sequence == 4:
        return 'Quarta'    
    return sequence


@bp.route('/<int:id>')
@login_required
def display(id):
    plan = Plan.query.get(id)
    planForm = PlanForm(obj=plan)
    return render_template('plan.html', form=planForm, visits=plan.visits, patient=plan.patient, readonly=True )


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    plan = Plan.query.get(id)
    planForm = PlanForm(obj=plan)

    if request.method == 'GET':        
        return render_template('plan.html', form=planForm, patient=plan.patient, readonly=False)

    if planForm.validate_on_submit():
        
        planForm.populate_obj(plan)
        
        try:
            validate_plan(plan)
        except Exception as error:
            flash(error)
            return render_template('plan.html', form=planForm, patient=plan.patient, readonly=False)

        db.session.add(plan)
        db.session.commit()

        flash('Plano foi atualizado com sucesso!')
        return redirect(url_for('patient.plans', id=plan.patient_id))

    flash('Erro não foi possível atualizar o plano!')
    return render_template('plan.html', form=planForm, patient=plan.patient, readonly=False)


@bp.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    plan = Plan.query.get(id)

    if not plan:
        # abort(404)
        return
    
    patient = plan.patient

    if (len( plan.visits ) > 0):
        flash('Não foi possivel excluir o plano, Existe consulta vinculada ao plano!')
        return redirect(url_for('patient.plans', id=patient.id))

    db.session.delete(plan)
    db.session.commit()
    flash('Plano foi excluido com sucesso!')

    return redirect(url_for('patient.plans', id=patient.id))


@bp.route('/<int:id>/visit', methods=('GET', 'POST'))
def visit(id):
    plan = Plan.query.get(id)

    visit = Visit()
    visitForm = VisitForm()

    if request.method == 'GET':
        tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(tz=tz)
        visit.date = now.date()
        visit.time = now.time()
        visit.sequence_number = len(plan.visits) + 1
        visitForm = VisitForm(obj=visit)
        return render_template('visit.html', form=visitForm, plan=plan)
        
    if visitForm.validate_on_submit():        
        visitForm.populate_obj(visit)
        
        try:
            validate_new_visit(visit, plan)
        except ValidationError as error:
            flash(error)
            return render_template('visit.html', form=visitForm, plan=plan)

        visit.plan = plan
        
        db.session.add(visit)
        db.session.commit()
        flash('Consulta registrada com sucesso!')
        return redirect(url_for('patient.plans', id=plan.patient_id))

    flash('Erro não foi possível registrar consulta!')   
    return render_template('visit.html', form=visitForm, plan=plan)


@bp.route('json/<int:id>')
def display_json(id):
    
    if request.is_json:
        return request.get_json()
    
    return 'OI'

class PlanForm(FlaskForm):
    plan_type = SelectField('Plano', choices=PlanType.choices())
    payment_type = SelectField('Forma de Pagamento', choices=PaymentType.choices())
    value = DecimalField('Valor')
    additional_payment_type = SelectField('Forma de Pagamento Adicional', choices=AdditionalPaymentType.choices())
    additional_value = DecimalField('Valor Adicional')
    total_amount = DecimalField('Total')
    receipt = BooleanField('Recibo')
    paid = BooleanField('Pago')
    expiry_date = DateField('Validade', format='%d/%m/%Y', validators=[DataRequired()])
    note = TextAreaField('Notas')
