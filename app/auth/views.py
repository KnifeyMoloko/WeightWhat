from flask import render_template, redirect, flash, session, url_for
from app import db
from app.db_models import User
from app.main.forms import RegisterForm
from . import auth


@auth.route('/register', methods=['GET', 'POST'])
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
    return render_template('auth/register.html', reg_form=reg_form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')


@auth.route('/logout', methods=['GET'])
def logout():
    return render_template('auth/logout.html')

