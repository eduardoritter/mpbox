from mpbox.models import Patient, User
from mpbox.core import Service

class PatientService(Service):
    __model__ = Patient

    def __init__(self, *args, **kwargs):
        super(PatientService, self).__init__(*args, **kwargs)

class UserService(Service):
    __model__ = User

    def __init__(self, *args, **kwargs):
        super(UserService, self).__init__(*args, **kwargs)