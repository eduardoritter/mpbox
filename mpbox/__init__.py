from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/hi")
    def hello():
        return "Hi, I'm up!"


    from mpbox import patient
   
    app.register_blueprint(patient.bp)

    # make url_for('index') == url_for('patient.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
