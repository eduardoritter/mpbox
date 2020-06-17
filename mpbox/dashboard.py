from datetime import datetime
from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_login import login_required

from mpbox.model import Plan, Visit
from mpbox.config import BASE_URL_PREFIX


bp = Blueprint('dashboard', __name__, url_prefix=BASE_URL_PREFIX + 'dashboard')


@bp.route('/')
@login_required
def dashboard():
    last_plans = Plan.query.order_by(Plan.created.desc()).limit(5)    
    return render_template('dashboard.html', last_plans=last_plans)


@bp.route('/search')
@login_required
def search():
    try:
        visit_date = datetime.strptime(request.args.get('visit_date'), '%d/%m/%Y')
        visits = Visit.query.filter(Visit.date == visit_date.date())
    except Exception as error:
        flash(error)
        return render_template('dashboard.html')
    
    return render_template('dashboard.html', visits=visits)


@bp.route('/unpaid')
def pending_plans():
    unpaid_plans = Plan.query.filter(Plan.paid == False)
    return render_template('dashboard.html', last_plans=unpaid_plans)


@bp.route('/expired')
@login_required
def expired_plans():
    return