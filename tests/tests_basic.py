"""Basic tests for the WeighWhat app."""

# imports
import unittest
from flask import current_app
from sqlalchemy_utils import database_exists, create_database
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        if not database_exists(self.app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(self.app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all(app=self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_app_has_db(self):
        self.assertTrue(db.exists)

    def test_secret_is_set(self):
        self.assertIsNotNone(self.app.config['SECRET_KEY'])
