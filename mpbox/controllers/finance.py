from flask import Blueprint, render_template

from mpbox.config import BASE_URL_PREFIX

bp = Blueprint('finance', __name__, url_prefix=BASE_URL_PREFIX + 'finance')


@bp.route('/')
def index():
    return render_template('finance.html')
