import unittest
from app.db_models import User


class UserModelTestCases(unittest.TestCase):
    """
    Test cases for the User database class.
    """
    def test_pswrd_setter(self):
        user = User(password='moving_w3ight')
        self.assertTrue(user.password is not None)

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
