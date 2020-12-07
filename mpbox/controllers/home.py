from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_login import login_required

from mpbox.models import Patient
from mpbox.services import patients, visits


bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/')
@login_required
def home():    
    return render_template('home.html', last_visits=visits.last())


@bp.route('/search')
@login_required
def search():
    name = request.args.get('name')    
    patient_list = patients.filter(Patient.name.like('%' + str(name) + '%')).all()

    if not patient_list:
        flash('Paciente %s não encontrado!' % name)
    else:
        patient_list.sort(key=lambda k: k.name)

    return render_template('home.html', patients=patient_list)


@bp.route('/ts')
def index():
    return render_template('index.html')