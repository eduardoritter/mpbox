from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


babel = Babel()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
