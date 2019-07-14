"""This is the core of the Flask application. This file defines
the app factory function and some other helper stuff that will
create the app instances according to the specifications in config.py"""

# imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_datepicker import datepicker
from config import config

# instantiate empty instances of flask extensions
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_mgmt = LoginManager()
login_mgmt.login_view = 'auth.login'


# this is the app factory function
def create_app(config_name):
    # init app with package name
    app = Flask(__name__)
    # import the app config from a config class
    app.config.from_object(config[config_name])
    # call the init_app function in the config class
    config[config_name].init_app(app)

    # since the app is now initiated and configured, add extensions to it
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_mgmt.init_app(app)

    # add datepicker and configure it
    dp = datepicker(app)
    datepicker.picker(dp, id='.dp', maxDate='2019-12-01', minDate='2019-01-01', btnsId='dpbtn')

    # only now can we import the blueprints that will use the app instance
    from .main import main as main_bp
    app.register_blueprint(main_bp)
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
