import enum

from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Column, Text, Numeric, Text, ForeignKey, Boolean, Enum, Date, Time
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin
from mpbox.extensions import db


class PaymentType(enum.Enum):
    DI = "Dinheiro"
    DB = "Débito"
    DP = "Depósito"
    CA = "Crédito a vista"
    C2 = "Crédito 2 parcelas"
    C3 = "Crédito 3 parcelas"
    C4 = "Crédito 4 parcelas"
    CO = "Cortesia"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    def __str__(self):
        return str(self.name)

    def __html__(self):
        return self.value

class AdditionalPaymentType(enum.Enum):
    NA = "Não Aplicável"
    DI = "Dinheiro"
    DB = "Débito"
    DP = "Depósito"
    CA = "Crédito a vista"
    C2 = "Crédito 2 parcelas"
    C3 = "Crédito 3 parcelas"
    C4 = "Crédito 4 parcelas"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    def __str__(self):
        return str(self.name)

    def __html__(self):
        return self.value

class PlanType(enum.Enum):
    P4 = "Pacote 4"
    P2 = "Consulta/Reconsulta"    
    IN = "Individual"
    AV = "Avaliação"

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
    birthdate = Column(Date)
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
    additional_payment_type = Column(Enum(AdditionalPaymentType))
    additional_value = Column(Numeric(precision=6, scale=2))
    total_amount = Column(Numeric(precision=6, scale=2))
    receipt = Column(Boolean, default=False)
    paid = Column(Boolean, default=True)
    expiry_date = Column(Date)
    note = Column(Text)
    visits = relationship("Visit", backref='plan')
    created = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)


class Visit(db.Model):
    __tablename__ = 'visit'
    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('plan.id'))
    sequence_number = Column(Integer, nullable=False)
    date = Column(Date)
    time = Column(Time)
    created = Column(DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    def gen_hash(self):
        self.password = pbkdf2_sha256.hash(self.password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)
