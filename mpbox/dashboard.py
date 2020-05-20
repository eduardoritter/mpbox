from flask import Blueprint, render_template, request, redirect, request, url_for, flash
from flask_login import login_required

from mpbox.model import Plan
from mpbox.config import BASE_URL_PREFIX


bp = Blueprint('dashboard', __name__, url_prefix=BASE_URL_PREFIX + 'dashboard')


@bp.route('/')
@login_required
def dashboard():
    last_plans = Plan.query.order_by(Plan.created.desc()).limit(5)    
    return render_template('dashboard.html', last_plans=last_plans)