from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def config_db(app):

    app.config.from_mapping(
        SECRET_KEY="secret",
        SQLALCHEMY_DATABASE_URI="sqlite:///mpbox.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    Migrate(app, db)