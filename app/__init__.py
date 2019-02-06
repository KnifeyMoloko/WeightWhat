"""This is the core of the Flask application. This file defines
the app factory function and some other helper stuff that will
create the app instances according to the specifications in config.py"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

# instantiate empty instances of flask extensions
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


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

    # only now can we import the bluepritns that will use the app instance
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    return app
