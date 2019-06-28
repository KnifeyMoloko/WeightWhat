import unittest
from flask import current_app
from sqlalchemy_utils import database_exists, create_database
from app import create_app, db
from app.db_models import User


class RegistrationTestCases(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        if not database_exists(self.app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(self.app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all(app=self.app)

        # register new user
        # login user
        # confirm user
        # login confirmed user

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        self.assertTrue(2 == 2)
