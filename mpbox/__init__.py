import os
import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel

app = Flask(__name__)
db = SQLAlchemy()

#babel = Babel(app)

app.config.from_mapping(
    SECRET_KEY="secret",
    SQLALCHEMY_DATABASE_URI="sqlite:///mpbox.sqlite",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    BABEL_DEFAULT_LOCALE="pt_BR",
    BABEL_DEFAULT_TIMEZONE="Brasilia"
)

db.init_app(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from mpbox import patient
app.register_blueprint(patient.bp)

from mpbox import plan
app.register_blueprint(plan.bp)

from mpbox import visit
app.register_blueprint(visit.bp)

from mpbox import auth
app.register_blueprint(auth.bp)

# make url_for('index') == url_for('patient.index')
# in another app, you might define a separate main index here with
# app.route, while giving the blog blueprint a url_prefix, but for
# the tutorial the blog will be the main index
app.add_url_rule("/", endpoint="patient.index")

@app.route("/hi")
def hello():
    return "Hi, I'm up!"