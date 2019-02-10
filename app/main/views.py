from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..db_models import Measurement, User
from ..email import send_email
from . import main
from .forms import LoginForm, DateForm, RegisterForm
#from .plots import plot_png


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
            # TODO: redirect to the user dashboard page

    return render_template('index.html', login_form=login_form, date_form=date_form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()

    if reg_form.validate_on_submit():
        name = User.query.filter_by(name=reg_form.username.data).first()
        if name is None:
            if reg_form.password.data == reg_form.password_confirmation.data:
                new_user = User(name=reg_form.username.data, password=reg_form.password.data)
                db.session.add(new_user)
                db.session.commit()
                session['user_name'] = name
                flash("New user added to database.")
            elif reg_form.password.data != reg_form.password_confirmation.data:
                flash("Password and Password Confirmation fields do not match. Please re-enter.")
                reg_form.password = None
                reg_form.password_confirmation = None
            else:
                return redirect(url_for('.internal_server_error'), 500)
        else:
            flash("This user name is already taken! Please choose a different user name.")
            reg_form.username.data = None
    else:
        flash("Validations failed. Try again.")
        reg_form.username = None
        reg_form.password = None
    return render_template('register.html', reg_form=reg_form)
