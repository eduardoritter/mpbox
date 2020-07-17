from .models import Patient
from .core import Service

class PatientService(Service):
    __model__ = Patient

    def __init__(self, *args, **kwargs):
        super(PatientService, self).__init__(*args, **kwargs)
