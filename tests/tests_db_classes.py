"""unittest tests for the db model classes for WeightWhat"""

# imports
import unittest
import time
from app import db
from app.db_models import User
from sqlalchemy_utils import database_exists, create_database
from app import create_app, db


class UserModelTestCases(unittest.TestCase):
    """
    Test cases for the User database class.
    """
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        if not database_exists(self.app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(self.app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all(app=self.app)

        self.user_1 = User(
            email="virginia.wolf@gmail.com",
            name='Virginia Wolf',
            password='t0_3dgy_4_U')
        self.user_2 = User(name="James Joyce",
                      email='joyce@finneganswake.com',
                      password='Dublin00')
        self.user_3 = User(
            email='mann.thomas@hotmail.com',
            name='Thomas Mann',
            password='Dublin00'
                      )
        db.session.add(self.user_1)
        db.session.add(self.user_2)
        db.session.add(self.user_3)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_pswrd_setter(self):
        self.assertIsNotNone(self.user_1.user_pswrd)

    def test_pswrd_is_not_directly_available(self):
        with self.assertRaises(AttributeError):
            self.user1.password

    def test_pswrd_salt_is_random(self):
        self.assertTrue(self.user_2.user_pswrd != self.user_3.user_pswrd)

    def test_pswrd_verification(self):
        self.assertTrue(self.user_2.verify_password('Dublin00'))
        self.assertFalse(self.user_2.verify_password('Cork00'))

    def test_create_token(self):
        self.assertIsNotNone(self.user_1.create_auth_token())

    def test_token_authentication(self):
        token = self.user_3.create_auth_token()
        self.assertTrue(self.user_3.validate_auth_token(token))

    def test_token_authentication_updates_user_confirmation(self):
        token = self.user_1.create_auth_token()
        self.user_1.validate_auth_token(token)
        db.session.commit()
        self.assertTrue(self.user_1.user_confirmed)

    def test_invalid_token(self):
        token = self.user_1.create_auth_token()
        # try to validate user 2 with user 1's token
        self.assertFalse(self.user_2.validate_auth_token(token))

    def test_token_timeout(self):
        token = self.user_1.create_auth_token(timeout=1)
        time.sleep(2)
        self.assertFalse(self.user_1.validate_auth_token(token))

