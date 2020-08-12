import pytz
from datetime import datetime
from sqlalchemy.sql import exists
from validate_docbr import CPF

from mpbox.models import Patient, Plan, Visit, User
from mpbox.core import Service
from mpbox.utils import ValidationError, validate_visit, validate_plan
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

    def delete(self, model):
        if (len( model.plans ) > 0):
            raise ValidationError('Não foi possivel excluir o paciente %s, Existe plano vinculado ao paciente!' % model.name)   
            
        super.delete(model)


class PlanService(Service):
    __model__ = Plan

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, model):
        validate_plan(model)
        super().save(model)

    def delete(self, model):
        if (len( model.visits ) > 0):
            raise ValidationError('Não foi possivel excluir o plano, Existe consulta vinculada ao plano!')
            
        super.delete(model)


class VisitService(Service):
    __model__ = Visit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    def new(self, plan=None, **kwargs):
        
        visit = super().new(**kwargs)

        if plan:
            visit.sequence_number = len(plan.visits) + 1
            now = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
            visit.date = now.date()
            visit.time = now.time()

        return visit
    
    def create(self, model):

        for visit in model.plan.visits:
            if id(model) != id(visit):
                if model.date == visit.date:                
                    raise ValidationError('Já existe consulta registrada na data ' + visit.date.strftime("%d/%m/%Y"))

        self.save(model)

    def save(self, model):
        validate_visit(model)
        super().save(model)


class UserService(Service):
    __model__ = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)