from flask_wtf import FlaskForm, Form

from wtforms import SelectField, TextField, StringField, TextAreaField, BooleanField, DecimalField, DateField, TimeField, validators
from wtforms.validators import DataRequired

from mpbox.models import PlanType, PaymentType, AdditionalPaymentType


class PlanForm(FlaskForm):
    plan_type = SelectField('Plano', choices=PlanType.choices())
    payment_type = SelectField('Forma de Pagamento', choices=PaymentType.choices())
    value = DecimalField('Valor')
    additional_payment_type = SelectField('Forma de Pagamento Adicional', choices=AdditionalPaymentType.choices())
    additional_value = DecimalField('Valor Adicional')
    total_amount = DecimalField('Total')
    receipt = BooleanField('Recibo')
    paid = BooleanField('Pago')
    expiry_date = DateField('Validade', format='%d/%m/%Y', validators=[DataRequired()])
    note = TextAreaField('Notas')


class VisitForm(FlaskForm):
    sequence_number = SelectField('Consulta', choices=[(1, 'Primeira'), (2, 'Segunda'), (3, 'Terceira'), (4, 'Quarta')], coerce=int)
    date = DateField('Data', format='%d/%m/%Y', validators=[DataRequired()])
    time = TimeField('Hora', validators=[DataRequired()])
    no_show = BooleanField('Não Compareceu')
    note = TextAreaField('Notas')


class PatientForm(FlaskForm):
    name = StringField('Nome', validators=[validators.required()])
    cpf = StringField('CPF', validators=[validators.required()])
    email = StringField('Email', validators=[validators.Email(), validators.required()])
    birthdate = DateField('Data de Nascimento', format='%d/%m/%Y', validators=[validators.required()])
    note = TextAreaField('Notas')