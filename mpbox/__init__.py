import os
import logging

from flask import Flask
from mpbox.db import config_db
from mpbox.auth import init_login_manager


def create_app( ):
    app = Flask(__name__)

    config_db(app)
    register_blueprints(app)
    init_login_manager(app)
       
    return app


def register_blueprints(app):
    """Register blueprints with the Flask application."""

    base = '/mpbox/'
   
    from mpbox import auth
    app.register_blueprint(auth.bp, url_prefix=base)

    from mpbox import home
    app.register_blueprint(home.bp, url_prefix=base + 'home')

    from mpbox import patient
    app.register_blueprint(patient.bp, url_prefix=base + 'patient')

    from mpbox import plan
    app.register_blueprint(plan.bp, url_prefix=base + 'plan')

    from mpbox import visit
    app.register_blueprint(visit.bp, url_prefix=base + 'visit')

    app.add_url_rule(base, endpoint='home.home')


if __name__ == "__main__":
	application = create_app( )
	application.run()