from flask import Blueprint

profile_settings = Blueprint('profile_settings', __name__)

from . import views
