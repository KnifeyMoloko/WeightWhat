from flask import Blueprint


# Blueprints generally are placed inside the __init__.py files
# create a new Blueprint instance to register the predefined views and errors

main = Blueprint('main', __name__)

from . import errors, views
