import os
from flask_migrate import Migrate
from flask_datepicker import datepicker
from app import create_app, db
from app.db_models import User, Measurement


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
dp = datepicker(app)
datepicker.picker(dp, id='.dp', maxDate='2019-07-01', minDate='2018-10-01', btnsId='dpbtn')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Measurement=Measurement)


@app.before_first_request
def create_db():
    db.create_all(app=app)


@app.cli.command()
def test():
    """Running unit tests for WeightWhat"""
    import unittest
    # defines where to look for tests in root
    tests = unittest.TestLoader().discover('tests')

    # run the test
    unittest.TextTestRunner(verbosity=2).run(tests)
