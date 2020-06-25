from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import config

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()


login_manager.login_view = 'users.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify()
        sslify.init_app(app)

    from .core import core
    from .costs import costs
    from .needs import needs
    from .users import users
    from .groups import groups
    from .api import api

    app.register_blueprint(core)
    app.register_blueprint(costs)
    app.register_blueprint(users)
    app.register_blueprint(needs)
    app.register_blueprint(groups)
    app.register_blueprint(api, url_prefix='/api')

    return app
