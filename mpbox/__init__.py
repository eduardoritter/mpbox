import os
import logging

from flask import Flask
from mpbox.extensions import db, babel, migrate, login_manager


def create_app( ):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="secret",
        SQLALCHEMY_DATABASE_URI="sqlite:///mpbox.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        BABEL_DEFAULT_LANGUAGE='pt_BR',
        BABEL_DEFAULT_TIMEZONE='America/Sao_Paulo',
    )

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