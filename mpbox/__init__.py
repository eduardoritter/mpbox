import os
import logging

from flask import Flask
from mpbox.db import config_db
from mpbox.auth import init_login_manager


def create_app( ):
    app = Flask(__name__)

    config_db(app)
    init_login_manager(app)

    from mpbox import auth
    app.register_blueprint(auth.bp)

    from mpbox import patient
    app.register_blueprint(patient.bp)

    from mpbox import plan
    app.register_blueprint(plan.bp)

    from mpbox import visit
    app.register_blueprint(visit.bp)



    # make url_for('index') == url_for('patient.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="patient.index")

    @app.route("/hi")
    def hello():
        return "Hi, I'm up!"
    
    return app


if __name__ == "__main__":
	application = create_app( )
	application.run()