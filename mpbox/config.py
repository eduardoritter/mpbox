
def config_app(app):

    app.config.from_mapping(
        SECRET_KEY="secret",
        SQLALCHEMY_DATABASE_URI="sqlite:///mpbox.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        BABEL_DEFAULT_LANGUAGE='pt_BR',
        BABEL_DEFAULT_TIMEZONE='America/Sao_Paulo',
    )