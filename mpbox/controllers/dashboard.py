from datetime import datetime
from flask import Blueprint, render_template, request, flash
from flask_login import login_required

from mpbox.models.model import Plan, Visit
from mpbox.config import BASE_URL_PREFIX
from mpbox.services import plans, visits


bp = Blueprint('dashboard', __name__, url_prefix=BASE_URL_PREFIX + 'dashboard')


@bp.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', last_plans=plans.last())


@bp.route('/search')
@login_required
def search():
    try:
        visit_date = datetime.strptime(request.args.get('visit_date'), '%d/%m/%Y')
        visit_list = visits.filter(Visit.date == visit_date.date())
    except Exception as error:
        flash(error)
    
    return render_template('dashboard.html', visits=visit_list)


@bp.route('/unpaid')
@login_required
def pending_plans():
    unpaid_plans = plans.filter(Plan.paid is False)
    return render_template('dashboard.html', last_plans=unpaid_plans)


@bp.route('/expired')
@login_required
def expired_plans():
    return