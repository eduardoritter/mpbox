from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Column, Text, Numeric, Text, ForeignKey, Boolean, Enum
from mpbox import db

class Patient(db.Model):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    cpf = Column(String, nullable=False)
    email = Column(String)
    note = Column(Text)
    created = Column(DateTime, default=datetime.utcnow)
