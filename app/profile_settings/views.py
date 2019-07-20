from flask import render_template, url_for
from flask_login import login_required, current_user
from app.db_models import User
from . import profile_settings
from .forms import ProfileForm


@profile_settings.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    profile_form = ProfileForm()
    profile_form.populate_placeholders(user=user)
    return render_template('profile_settings/settings.html', user=user, profile_form=profile_form)

