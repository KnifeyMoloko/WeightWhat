from flask import render_template, redirect, flash, session, url_for, request
from flask_login import login_required, login_user, logout_user
from app import db
from app.db_models import User
from app.main.forms import RegisterForm, LoginForm
from . import auth


@auth.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        name = User.query.filter_by(email=reg_form.username.data).first()
        if name is None:
            if reg_form.password.data == reg_form.password_confirmation.data:
                new_user = User(email=reg_form.email.data,
                                name=reg_form.username.data,
                                password=reg_form.password.data)
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
            flash("This email was already used! Please use a different email.")
            reg_form.username.data = None
    return render_template('auth/register.html', reg_form=reg_form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
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
                next = url_for('main.index')
            return redirect(next)
        else:
            redirect('main.internal_server_error')
    return render_template('auth/login.html')


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out")
    return redirect(url_for('main.index'))

