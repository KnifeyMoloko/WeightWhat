from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask_login import login_required, login_user
from .. import db
from ..db_models import Measurement, User
from ..email import send_email
from . import main
from .forms import DateForm
from ..auth.forms import LoginForm


# from .plots import plot_png


@main.route('/', methods=['GET', 'POST'])
def index():
    date_form = DateForm()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("I don't know you! No user with this email account registered.")
        elif user is not None and not user.verify_password(form.pswrd.data):
            flash("Incorrect password!")
        elif user is not None and user.verify_password(form.pswrd.data):
            login_user(user, form.keep_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.user_dash', user_id=user.id)
            return redirect(next)
        else:
            redirect('main.internal_server_error')
    else:
        for error in form.errors.items():
            flash("Something went wrong in {f} field: {m}".format(
                f=error[0], m=error[1][0]))
    return render_template('index.html', login_form=form, date_form=date_form)


@main.route('/plot')
@login_required
def plot_page():
    return render_template('base.html')


@main.route('/<user_id>/dashboard', methods=['GET', 'POST'])
@login_required
def user_dash(user_id):
    uid = user_id
    name = User.query.filter_by(id=uid).first().name
    return render_template('dashboard.html', name=name, uid=uid)
