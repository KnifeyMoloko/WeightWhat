"""
Define error handling responses for the main views here.
Imported via the main Blueprint.
"""

from flask import render_template
from . import main
"""This is confusing: main is defined in the Blueprint
file (__init__.py) and imported here. But it also imports
the functions defined here. Cyclical much?"""


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
