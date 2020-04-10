import enum

from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Column, Text, Numeric, Text, ForeignKey, Boolean, Enum, Date, Time
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin
from mpbox.db import db

class PaymentType(enum.Enum):
    DI = "Dinheiro"
    DB = "Debito"
    DP = "Deposito"
    CA = "Credito A vista"
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

class AdditionalPaymentType(enum.Enum):
    NA = "Não Aplicável"
    DI = "Dinheiro"
    DB = "Debito"
    DP = "Deposito"
    CA = "Credito A vista"
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
    note = Column(Text)
    visits = relationship("Visit", backref='plan')
    created = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)


class Visit(db.Model):
    __tablename__ = 'visit'
    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('plan.id'))
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

class Log(db.Model):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    table = Column(String)
    detail = Column(String)
    created = Column(DateTime, default=datetime.utcnow)
