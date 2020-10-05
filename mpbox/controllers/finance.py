from flask import Blueprint, render_template


bp = Blueprint('finance', __name__, url_prefix='/finance')


@bp.route('/')
def index():
    return render_template('finance.html')
