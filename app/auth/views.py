import time
from flask import render_template, redirect, flash, session, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from app import db
from app.db_models import User
from app.email import send_email
from .forms import RegisterForm, LoginForm
from . import auth


@auth.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        name = User.query.filter_by(email=reg_form.username.data).first()
        if name is None:
            new_user = User(email=reg_form.email.data,
                            name=reg_form.username.data,
                            password=reg_form.password.data)
            db.session.add(new_user)
            db.session.commit()
            token = new_user.create_auth_token()
            send_email(new_user.email, "Welcome to WeightWhat", 'auth/mail/confirm',
                       user=new_user, token=token)
            flash("Good job! A confirmation e-mail has been sent out to your e-mail account. "
                  "Please click on the link in that e-mail")
            return redirect(url_for('main.index'))
        else:
            flash("This email was already used! Please use a different email.")
            reg_form.username.data = None

    for error in reg_form.errors.items():
        flash("Something went wrong in field {f}: {m}".format(f=error[0], m=error[1][0]))

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
            redirect(url_for('main.internal_server_error'))
    return render_template('auth/login.html')


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out")
    return redirect(url_for('main.index'))


@auth.route('/account_confirmation/<token>')
@login_required
def account_confirmation(token):
    if current_user.user_confirmed:
        return redirect(url_for('main.index'))
    if current_user.validate_auth_token(token):
        db.session.commit()  # this finalizes the changes made by the .confirm method in User
        flash("You're so cool! Welcome aboard, user account authentication is now complete. Enjoy the app!")
    else:
        flash("Oh-oh! Something went wrong. You're authentication token has expired or was invalid. Please retry!")
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.user_confirmed and request.blueprint != 'auth':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.user_confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/resend')
@login_required
def resend():
    token = current_user.create_auth_token()
    send_email(current_user.email, "Welcome to WeightWhat", 'auth/mail/confirm',
               user=current_user, token=token)
    flash("A new confirmation e-mail has been sent out to your e-mail account. "
          "Please click on the link in that e-mail")
    return redirect(url_for('main.index'))
