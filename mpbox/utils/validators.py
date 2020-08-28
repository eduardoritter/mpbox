import pytz
from datetime import datetime

from mpbox.models.model import PlanType, AdditionalPaymentType, PaymentType


class ValidationError(Exception):
    pass


def validate_plan(plan):

    plan_type = PlanType[plan.plan_type]
    payment_type = PaymentType[plan.payment_type]
    add_payment_type = AdditionalPaymentType[plan.additional_payment_type]

    if plan_type is PlanType.IN or plan_type is PlanType.AV:
        if len(plan.visits) > 1:
            raise Exception('Não é possivel alterar o Tipo do Plano, Existe(m) consulta(s) vinculada(s) ao plano!')

    if plan_type is PlanType.P2:
        if len(plan.visits) > 2:
            raise Exception('Não é possivel alterar o Tipo do Plano, Existe(m) consulta(s) vinculada(s) ao plano!')

    if payment_type is PaymentType.CO:
        if plan.value > 0:
            raise Exception('Plano Cortesia, campo valor dever estar zerado!')
    else:
        if plan.value == 0:
            raise Exception('Informe o valor!')

    if add_payment_type is AdditionalPaymentType.NA:
        if plan.additional_value > 0:
            raise Exception('Verifique a Forma de Pagamento Adicional!')
    else:
        if plan.additional_value == 0:
            raise Exception('Verifique a Forma de Pagamento Adicional!')


def validate_visit(visit):
    now = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))

    if visit.date > now.date():
        raise ValidationError('Não é possivel registrar consulta no futuro!')

    if visit.sequence_number > len(visit.plan.visits):
        raise ValidationError('Verifique o número de sequência da consulta!')

    if visit.date > visit.plan.expiry_date:
        raise ValidationError('Plano expirado! Não é possivel registrar a consulta.')
