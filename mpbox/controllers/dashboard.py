from datetime import datetime
from flask import Blueprint, render_template, request, flash
from flask_login import login_required

from mpbox.models.model import Plan, Visit
from mpbox.services import plans, visits
from mpbox.utils import week_dates


bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', last_plans=plans.last())


@bp.route('/week_visits')
@login_required
def week_visits():
    week = request.args.get('week')
    year = request.args.get('year')

    print(week)
    print(year)

    for day in week_dates(week=week, year=year):
        print(day)
        # try:
        #     visit_list = visits.filter(Visit.date == day)
        #     print(visit_list)
        # except Exception as error:
        #     flash(error)

    return render_template('dashboard.html')


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