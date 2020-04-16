from mpbox.model import PlanType, AdditionalPaymentType, PaymentType
from validate_docbr import CPF

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

