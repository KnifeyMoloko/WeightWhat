from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..db_models import Measurement, User
from ..email import send_email
from . import main
from .forms import LoginForm, DateForm
#from .plots import plot_png


@main.route('/', methods=['GET', 'POST'])
def index():
    date_form = DateForm()
    login_form = LoginForm()
    return render_template('index.html', login_form=login_form, date_form=date_form)
