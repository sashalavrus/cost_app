import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['COSTAPP_ADMIN'] = 'grifin07@mail.com'
app.config['COSTAPP_MAIL_SUBJECT_PREFIX'] = '[CostApp]'
app.config['COSTAPP_MAIL_SENDER'] = 'costapp2020@gmail.com'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'costapp2020@gmail.com'
app.config['MAIL_PASSWORD'] = 'pk340ak47'


##DATABASE

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
mail = Mail()
mail.init_app(app)
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

from .core import core
from .costs import costs
from .needs import needs
from .users import users
from .groups import groups

app.register_blueprint(core)
app.register_blueprint(costs)
app.register_blueprint(users)
app.register_blueprint(needs)
app.register_blueprint(groups)
