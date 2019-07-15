"""Unit tests for email features for WeightWhat app."""

import imaplib
import unittest
import email as em
from time import sleep
from sqlalchemy_utils import database_exists, create_database
from app import create_app, db, email
from app.db_models import User


class EmailTestCases(unittest.TestCase):
    def setUp(self):
        # use 'testing_with_email' for compatibility with flask-mail
        self.app = create_app('testing_with_email')
        self.app_context = self.app.app_context()
        self.app_context.push()

        #  make sure a database exists for testing (defaults to SQLite)
        if not database_exists(self.app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(self.app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all(app=self.app)

        # config the email account to be checked for incoming emails
        self.mail_pass = self.app.config['MAIL_PASSWORD']
        self.smtp_server = 'imap.gmail.com'
        self.smtp_port = 993

        self.user_1 = User(
            name='KnifeyTest',
            email=self.app.config['MAIL_USERNAME'],
            password='HaltAndCatchFire'
        )
        db.session.add(self.user_1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_sending_email(self):
        """
        Tests if the app can send verification emails.
        """
        token = self.user_1.create_auth_token()
        email.send_email(self.user_1.email,
                         subject="",
                         user=self.user_1,
                         token=token,
                         template='auth/mail/confirm')
        sleep(60)
        msg = self.check_mail(self.user_1)
        self.assertIsInstance(msg, em.message.Message)

    def check_mail(self, user):
        """
        Connects to test gmail account and returns the first message
        with the subject specified in the config file.
        """
        mail = imaplib.IMAP4_SSL(host=self.smtp_server, port=self.smtp_port)
        mail.login(user.email, self.mail_pass)
        mail.select('inbox')

        # charset and data to retrieve
        t, data = mail.search(None, 'SUBJECT "{} "'.format(self.app.config['MAIL_SUBJECT_PREFIX']))

        # get the id of the latest message that is stored in data
        latest = data[0].split()[-1]

        # fetch the email with the latest id
        typ, msg_data = mail.fetch(latest, '(RFC822)')

        # convert message data into an emial package message object
        return_msg = em.message_from_bytes(msg_data[0][1])
        return return_msg
