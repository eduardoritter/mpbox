import os
import logging

from flask import Flask
from mpbox.config import config_app, BASE_URL_PREFIX
from mpbox.extensions import db, babel, migrate, login_manager


def create_app( ):
    app = Flask(__name__)

    config_app(app)
    register_extensions(app)
    register_blueprints(app)
       
    return app

def register_extensions(app):
    """Register extensions with the Flask application."""
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


def register_blueprints(app):
    """Register blueprints with the Flask application."""
   
    from mpbox import auth
    app.register_blueprint(auth.bp)

    from mpbox import dashboard
    app.register_blueprint(dashboard.bp)

    from mpbox import home
    app.register_blueprint(home.bp)

    from mpbox import patient
    app.register_blueprint(patient.bp)

    from mpbox import plan
    app.register_blueprint(plan.bp)

    from mpbox import visit
    app.register_blueprint(visit.bp)

    app.add_url_rule(BASE_URL_PREFIX, endpoint='home.home')


if __name__ == "__main__":
	application = create_app( )
	application.run()