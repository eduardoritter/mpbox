import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta

from mpbox.models.model import PlanType


def is_active_plan(plan):

    if now().date() > plan.expiry_date:
        return False

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

def classify_plans(plans):

    active_plans = []
    old_plans = []

    for p in plans:
        if is_active_plan(p):
            active_plans.append(p)
        else:
            old_plans.append(p)

    return active_plans, old_plans

def now():
    return datetime.now(tz=pytz.timezone('America/Sao_Paulo'))

def six_months_from_now():
    return now().date() + relativedelta(months=6)