from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_login import login_required

from mpbox.models.model import Patient, Visit
from mpbox.config import BASE_URL_PREFIX


bp = Blueprint('home', __name__, url_prefix=BASE_URL_PREFIX + 'home')


@bp.route('/')
@login_required
def home():
    lastVisits = Visit.query.order_by(Visit.created.desc()).limit(5)    
    return render_template('home.html', lastVisits=lastVisits)


@bp.route('/search')
@login_required
def search():
    name = request.args.get('name')    
    patients = Patient.query.filter(Patient.name.like('%' + str(name) + '%')).all()

    return render_template('home.html', patients=patients)