import pytz
from datetime import datetime
from validate_docbr import CPF
from sqlalchemy import inspect

from mpbox.model import PlanType, AdditionalPaymentType, PaymentType


class ValidationError(Exception):
    pass

def validate_patient(patient):
    
    cpf = CPF()

    if not cpf.validate(patient.cpf):
        raise Exception('CPF inválido!')


def validate_plan(plan):
    
    if plan.plan_type == PlanType.IN.name or plan.plan_type == PlanType.AV.name:
        if len(plan.visits) > 1:
            raise Exception('Não foi possivel modificar o Tipo do Plano, Existem consultas vinculadas ao plano!')

    if plan.payment_type == PaymentType.CO.name:
        if plan.value > 0:
            raise Exception('Plano Cortesia campo valor dever estar zerado!')

    if plan.additional_value == 0:
        if plan.additional_payment_type != AdditionalPaymentType.NA.name:
            raise Exception('Verifique a Forma de Pagamento Adicional!')
    else:
        if plan.additional_payment_type == AdditionalPaymentType.NA.name:
            raise Exception('Informe a Forma de Pagamento Adicional!')


def validate_new_visit(visit, plan):

    validate_visit(visit, plan)

    for v in plan.visits:
        if v.date == visit.date:                
            raise ValidationError('Já existe consulta registrada na data ' + visit.date.strftime("%d/%m/%Y"))

def validate_visit(visit, plan=None):
    now = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))

    if visit.date > now.date():
        raise ValidationError('Não é possivel registrar consulta no futuro!')

    if plan:
        expiry_date = plan.expiry_date
    else:
        expiry_date = visit.plan.expiry_date
    
    if visit.date > expiry_date:
        raise ValidationError('Plano expirado! Não é possivel registrar a consulta.')


def is_active_plan(plan):

    if (plan.plan_type == PlanType.P2 and
            len(plan.visits) < 2):
        return True

    if (plan.plan_type == PlanType.P4 and
            len(plan.visits) < 4):
        return True
    
    if (plan.plan_type == PlanType.IN and
            len(plan.visits) < 1):
        return True

    if (plan.plan_type == PlanType.AV and
            len(plan.visits) < 1):
        return True
    
    return False


def has_active_plan(plans):
   
    for plan in plans:
        if is_active_plan(plan):
            return True
    
    return False

