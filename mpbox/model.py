import enum

from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Column, Text, Numeric, Text, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship

from mpbox import db

class PaymentType(enum.Enum):
    DI = "Dinheiro"
    DB = "Debito"
    CA = "Credito Avista"
    C2 = "Credito 2 Parcelas"
    C3 = "Credito 3 Parcelas"
    C4 = "Credito 4 Parcelas"
    CO = "Cortesia"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    def __str__(self):
        return str(self.name)

    def __html__(self):
        return self.value

class PlanType(enum.Enum):
    IN = "Individual"
    P2 = "Consulta/Reconsulta"
    P4 = "Pacote 4"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
    
    def __str__(self):
        return str(self.name)
    
    def __html__(self):
        return self.value

class Patient(db.Model):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    cpf = Column(String, nullable=False)
    email = Column(String)
    plans = relationship("Plan", backref='patient')
    inactive = Column(Boolean, default=False)
    note = Column(Text)
    created = Column(DateTime, default=datetime.utcnow)


class Plan(db.Model):
    __tablename__ = 'plan'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    plan_type = Column(Enum(PlanType), nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)
    value = Column(Numeric(precision=6, scale=2))
    receipt = Column(Boolean, default=False)
    note = Column(Text)
    visits = relationship("Visit", backref='plan')
    created = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)


class Visit(db.Model):
    __tablename__ = 'visit'
    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('plan.id'))
    created = Column(DateTime, default=datetime.utcnow)
