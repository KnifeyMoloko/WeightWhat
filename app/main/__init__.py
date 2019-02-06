from flask import Blueprint


# create a new Blueprint instance to register the predefined views and errors

main = Blueprint('main', __name__)

from . import errors, views
