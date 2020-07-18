from mpbox.models import Patient, Plan, Visit, User
from mpbox.core import Service

class PatientService(Service):
    __model__ = Patient

    def __init__(self, *args, **kwargs):
        super(PatientService, self).__init__(*args, **kwargs)

class PlanService(Service):
    __model__ = Plan

    def __init__(self, *args, **kwargs):
        super(PlanService, self).__init__(*args, **kwargs)

class VisitService(Service):
    __model__ = Visit

    def __init__(self, *args, **kwargs):
        super(VisitService, self).__init__(*args, **kwargs)

class UserService(Service):
    __model__ = User

    def __init__(self, *args, **kwargs):
        super(UserService, self).__init__(*args, **kwargs)