"""This is the main orchestration file for the WeightWhat app.
It calls the app factory function with the imported config,
initiates the Migrate extension, creates the db if needed,
makes a shell context and exposes a 'test' CLI command."""

# imports
import os
from sqlalchemy_utils import create_database, database_exists
from flask_migrate import Migrate
from app import create_app, db
from app.db_models import User, Measurement

# create app instance by using the app factory function
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# initiate the Migrate extension for SQLAlchemy with the app instance
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Measurement=Measurement)


@app.before_first_request
def create_db():
    """This is a request hook - a function running outside and
    independently of any view function. In this case it creates
    a db if no db exists on the server for this app."""
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all(app=app)


@app.cli.command()
def test():
    """Running unit tests for WeightWhat"""
    import unittest
    # defines where to look for tests in root
    tests = unittest.TestLoader().discover('tests')

    # run the test
    unittest.TextTestRunner(verbosity=2).run(tests)
