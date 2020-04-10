from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import LoginManager, login_user, logout_user
from mpbox.model import User
from mpbox.db import db


bp = Blueprint('auth', __name__)
login_manager = LoginManager()


def init_login_manager(app):
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@bp.route('/signup')
def signup():
    return render_template('signup.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.verify_password(password):
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('patient.index'))

    flash('Please check your login details and try again.')
    return redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route('/create_user')
def create_user():

    user = User()

    user.username = 'ad'
    user.password = '123'
    user.gen_hash()

    db.session.add(user)
    db.session.commit()

    flash('User created.')
    return redirect(url_for('auth.login'))