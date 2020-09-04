from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_login import login_required

from mpbox.models import Patient
from mpbox.config import BASE_URL_PREFIX
from mpbox.services import patients, visits


bp = Blueprint('home', __name__, url_prefix=BASE_URL_PREFIX + 'home')


@bp.route('/')
@login_required
def home():    
    return render_template('home.html', last_visits=visits.last())


@bp.route('/search')
@login_required
def search():
    name = request.args.get('name')    
    patient_list = patients.filter(Patient.name.like('%' + str(name) + '%')).all()
    return render_template('home.html', patients=patient_list)


@bp.route('/ts')
def index():
    return render_template('index.html')