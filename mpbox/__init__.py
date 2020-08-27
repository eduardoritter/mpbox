from flask import Flask
from mpbox.config import config_app, BASE_URL_PREFIX
from mpbox.extensions import db, babel, migrate, login_manager


def create_app():
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
    import mpbox.controllers as controllers

    blueprints = controllers.default_blueprints

    if blueprints:
        for blueprint in blueprints:
            app.register_blueprint(blueprint)

    app.add_url_rule(BASE_URL_PREFIX, endpoint='home.home')


if __name__ == "__main__":
    application = create_app()
    application.run()