from flask import render_template, url_for
from flask_login import login_required, current_user
from app import db
from app.db_models import User
from . import profile_settings


@profile_settings.route('/', methods=['GET', 'POST'])
@login_required
def profile_settings():
    return render_template('profile_settings/settings.html')

