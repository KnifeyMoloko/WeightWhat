from flask import render_template, session, redirect, url_for, current_app, flash
from flask_login import login_required
from .. import db
from ..db_models import Measurement, User
from ..email import send_email
from . import main
from .forms import LoginForm, DateForm, RegisterForm


# from .plots import plot_png


@main.route('/', methods=['GET', 'POST'])
def index():
    # instantiate forms for user input
    date_form = DateForm()
    login_form = LoginForm()

    # check if the whole form passed validations
    if login_form.validate_on_submit():
        # get the user name from the form
        user = User.query.filter_by(name=login_form.user.data).first()

        # if the user's name was not in the db
        if user is None:
            # inform the user of the name not being recognized...
            print("User not found")
            flash("Are you new here? Click 'Register' to create an account.")
            session['user_known'] = False  # and set the user_known flag in session
        else:
            # the user was recognized, check password
            print("User found")
            session['user_known'] = True
            session['user_name'] = login_form.user.data

    return render_template('index.html', login_form=login_form, date_form=date_form)


@main.route('/plot')
@login_required
def plot_page():
    return render_template('base.html')
