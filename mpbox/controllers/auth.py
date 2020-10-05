from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required

from mpbox.services import users
from mpbox.extensions import login_manager


bp = Blueprint('auth', __name__)


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

    user = users.first(username=username)

    if user and user.verify_password(password):
        login_user(user)
        flash('Login efetuado com sucesso.')
        return redirect(url_for('home.home'))

    flash('Credenciais inválidas! Verifique e tente novamente.')
    return redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(id):
    return users.get(id)


@bp.route('/create_user', methods=['GET'])
@login_required
def create_user():

    username = request.args.get('username')
    password = request.args.get('password')
   
    if not username or not password:
        flash('User not created.')
        return redirect(url_for('auth.login'))

    user = users.new()

    user.username = username
    user.password = password
    user.gen_hash()

    users.save(user)

    flash('User created.')
    return redirect(url_for('auth.login'))