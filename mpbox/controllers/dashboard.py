from datetime import datetime
from flask import Blueprint, render_template, request, flash
from flask_login import login_required

from mpbox.models.model import Plan, Visit, PaymentType
from mpbox.services import plans, visits
from mpbox.utils import week_dates


bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', week_visits=_week_visits())


@bp.route('/last')
@login_required
def last_visits():
    return render_template('dashboard.html', last_plans=plans.last())


@bp.route('/week/<week_year>')
@login_required
def week_visit(week_year):

    year = int(week_year[:4])
    week = int(week_year[4:])

    return render_template('dashboard.html', week_visits=_week_visits(week, year))


@bp.route('/search')
@login_required
def search():
    visit_list = None
    try:
        visit_date = datetime.strptime(request.args.get('visit_date'), '%d/%m/%Y')
        visit_list = visits.filter(Visit.date == visit_date.date())
    except Exception as error:
        flash(error)

    if not list(visit_list):
        flash('Nenhuma consulta encontrada em %s!' % visit_date.strftime('%d/%m/%Y'))
    
    return render_template('dashboard.html', visits=visit_list)


@bp.route('/unpaid')
@login_required
def pending_plans():
    unpaid_plans = plans.filter(Plan.paid == False)
    return render_template('dashboard.html', last_plans=unpaid_plans)


@bp.route('/deposit')
@login_required
def deposit():
    deposit_plans = plans.filter(Plan.payment_type == PaymentType.DP)
    return render_template('dashboard.html', last_plans=deposit_plans)


@bp.route('/expired')
@login_required
def expired_plans():
    return


def _week_visits(week=None, year=None):

    week_visits = []

    for day in week_dates(week=week, year=year):
        day_visits = {}
        visit_list = []

        try:
            visit_list = list(visits.filter(Visit.date == day))
            visit_list.sort(key=lambda k: k.time)
        except Exception as error:
            flash(error)

        day_visits['day'] = day
        day_visits['visits'] = visit_list
        week_visits.append(day_visits)

    return week_visits
