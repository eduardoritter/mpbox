import os
import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    app.config.from_mapping(        
        SECRET_KEY="secret",        
        SQLALCHEMY_DATABASE_URI="sqlite:///mpbox.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )


    @app.route("/hi")
    def hello():
        return "Hi, I'm up!"

    db.init_app(app)
    Migrate(app, db)

    from mpbox import patient
   
    app.register_blueprint(patient.bp)

    from mpbox import plan

    app.register_blueprint(plan.bp)

    # make url_for('index') == url_for('patient.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="patient.index")

    return app
