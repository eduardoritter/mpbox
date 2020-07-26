import pytz
from datetime import datetime
from sqlalchemy.sql import exists
from validate_docbr import CPF

from mpbox.models import Patient, Plan, Visit, User
from mpbox.core import Service
from mpbox.utils import ValidationError, validate_visit
from mpbox.extensions import db


class PatientService(Service):
    __model__ = Patient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def save(self, model):
        cpf = CPF()

        if not cpf.validate(model.cpf):
            raise ValidationError('CPF inválido!')

        super().save(model)


    def create(self, model):
        if db.session.query(exists().where(Patient.cpf == model.cpf)).scalar():
            raise ValidationError('Paciente %s já registrado!' % model.name)

        self.save(model)


class PlanService(Service):
    __model__ = Plan

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def delete(self, model):
        if (len( model.visits ) > 0):
            raise ValidationError('Não foi possivel excluir o plano Existe consulta vinculada ao plano!')
            
        self.delete(model)


class VisitService(Service):
    __model__ = Visit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    def new(self, **kwargs):
        v = super().new(**kwargs)
        tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(tz=tz)
        v.date = now.date()
        v.time = now.time()
        return v


    def save(self, model):
        validate_visit(model)
        super().save(model)


class UserService(Service):
    __model__ = User

    def __init__(self, *args, **kwargs):
        super(UserService, self).__init__(*args, **kwargs)