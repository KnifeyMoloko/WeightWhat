import unittest

import time

from app import db
from app.db_models import User


class UserModelTestCases(unittest.TestCase):
    """
    Test cases for the User database class.
    """
    def test_pswrd_setter(self):
        user = User(password='moving_w3ight')
        self.assertTrue(user.user_pswrd is not None)

    def test_pswrd_is_not_directly_available(self):
        user = User(password='moving_w3ight')
        with self.assertRaises(AttributeError):
            user.password

    def test_pswrd_salt_is_random(self):
        user_one = User(password='moving_w3ight')
        user_two = User(password='moving_w3ight')
        self.assertTrue(user_one.user_pswrd != user_two.user_pswrd)

    def test_pswrd_verification(self):
        user = User(password='moving_w3ight')
        self.assertTrue(user.verify_password('moving_w3ight'))
        self.assertFalse(user.verify_password('moving_other_thing'))

    def test_token_authentication(self):
        user = User(password='JustGr8')
        db.session.add(user)
        db.session.commit()
        token = user.create_auth_token()
        self.assertTrue(user.validate_auth_token(token))

    def test_token_authentication_updates_user_confirmation(self):
        user = User(password='JustGr8')
        db.session.add(user)
        db.session.commit()
        token = user.create_auth_token()
        user.validate_auth_token(token)
        db.session.commit()
        self.assertTrue(user.user_confirmed)

    def test_invalid_token(self):
        user = User(password='NotF4n')
        user_k = User(password='JustSpl3ndid')
        db.session.add(user)
        db.session.commit()
        token = user_k.create_auth_token()
        self.assertFalse(user.validate_auth_token(token))

    def test_token_timeout(self):
        user = User(password='TimeByPinkFloyd')
        db.session.add(user)
        db.session.commit()
        token = user.create_auth_token(timeout=1)
        time.sleep(2)
        self.assertFalse(user.validate_auth_token(token))
