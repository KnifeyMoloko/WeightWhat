"""Unit tests for authentication features for WeightWhat app."""

import unittest
import email as em
from sqlalchemy_utils import database_exists, create_database
from app import create_app, db, mail, email
from app.db_models import User


class RegistrationTestCases(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        #  make sure a database exists for testing (defaults to SQLite)
        if not database_exists(self.app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(self.app.config['SQLALCHEMY_DATABASE_URI'])
        # create db tables from models
        db.create_all(app=self.app)

        # create test users in db and commits
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
        self.user_4 = User(
            email="knifey@moloko.com",
            name='KnifeyTest',
            password='HaltAndCatchFire'
        )
        db.session.add(self.user_1)
        db.session.add(self.user_2)
        db.session.add(self.user_3)
        db.session.add(self.user_4)
        db.session.commit()

        self.user_list = [self.user_1, self.user_2,
                          self.user_3, self.user_4]

        # TODO:login user
        # TODO:login confirmed user

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        """
        Test if users created in db are registered, i.e. active.
        """
        for user in self.user_list:
            self.assertTrue(user.is_active)

    def test_confirm_users(self):
        """
        Spoofs verification emails sending, then checks the emails
        for tokens and attempts to authenticate user accounts with
        them.
        """
        # use the record messages buffer to spoof an email server
        with mail.record_messages() as outbox:
            for user in self.user_list:
                email.send_email(to=user.email,
                                 subject="test_register_users",
                                 template='auth/mail/confirm',
                                 user=user,
                                 token=user.create_auth_token())
                # retrieve message for user
                msg = outbox[self.user_list.index(user)]

                # parse message for token
                token = self.parse_message(msg)
                self.assertTrue(user.validate_auth_token(token))
                self.assertTrue(user.user_confirmed)

    @staticmethod
    def parse_message(msg):
        """
        Parse flask-mail Message and extract token from it.
        """
        # recreate email object from flask-mail Message object
        message = em.message_from_string(str(msg))

        # get body from message
        if message.is_multipart():
            for part in message.walk():
                part_type = part.get_content_type()
                part_dispo = str(part.get('Content-Disposition'))

                if part_type == 'text/plain' and 'attachment' not in part_dispo:
                    body = part.get_payload(decode=False)
                    break
        else:
            body = message.get_payload(decode=False)

        # add 21 for chars in "accpunt_confirmation/"
        start = body.find("account_confirmation/") + 21
        end = body.find("Good luck")

        # extract token
        token = body[start:end].strip()
        return token

