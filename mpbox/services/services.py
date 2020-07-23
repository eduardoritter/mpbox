from sqlalchemy.sql import exists

from validate_docbr import CPF

from mpbox.models import Patient, Plan, Visit, User
from mpbox.core import Service
from mpbox.utils import ValidationError
from mpbox.extensions import db


class PatientService(Service):
    __model__ = Patient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def save(self, model):
        cpf = CPF()

        if not cpf.validate(model.cpf):
            raise ValidationError('CPF inválido!')

        super( ).save(model)


    def create(self, model):
        if db.session.query(exists().where(Patient.cpf == model.cpf)).scalar():
            raise ValidationError('Paciente %s já registrado!' % model.name)

        self.save(model)


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