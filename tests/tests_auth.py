import unittest
import imaplib
import smtplib
import email as em
from flask import current_app
from sqlalchemy_utils import database_exists, create_database
from app import create_app, db
from app.db_models import User


class RegistrationTestCases(unittest.TestCase):
    def setUp(self):
        # create app and push it to the app context stack
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        #  make sure a database exists for testing (defaults to SQLite)
        if not database_exists(self.app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(self.app.config['SQLALCHEMY_DATABASE_URI'])
        # create db tables from models
        db.create_all(app=self.app)

        # create test users in db; user_4 is for email testing
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
            name='KnifeyTest',
            email=self.app.config['MAIL_USERNAME'],
            password='HaltAndCatchFire'
        )
        db.session.add(self.user_1)
        db.session.add(self.user_2)
        db.session.add(self.user_3)
        db.session.commit()

        # config the email account to be checked for incoming emails
        self.mail_pass = self.app.config['MAIL_PASSWORD']
        self.smtp_server = 'imap.gmail.com'
        self.smtp_port = 993
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

    def test_email_returns_message(self):
        """
        Checks if there are valid authentication emails retrievable
        from a test email account. Does not validate the contents of
        the email.
        """
        self.assertIsInstance(self.check_mail(self.user_4),
                              em.message.Message)

    def test_body(self):
        self.assertIsInstance(
            self.parse_message(self.check_mail(self.user_4)),
            str
        )

    def check_mail(self, user):
        mail = imaplib.IMAP4_SSL(host=self.smtp_server, port=self.smtp_port)
        mail.login(user.email, self.mail_pass)

        mail.select('inbox')
        # charset and data to retrieve
        t, data = mail.search(None, 'SUBJECT "[WeightWhatApp] Welcome '
                                    'to WeightWhat"')
        # get the id of the latest message that is stored in data
        latest = data[0].split()[-1]
        """
        for i in range(id_list[0], id_list[-1]):
            typ, data = mail.fetch(i, '(RFC822')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = em.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From: ' + email_from + '\n')
                    print('Subject: ' + email_subject + '\n')
                    print('Message: ' + msg + '\n')
        """
        typ, msg_data = mail.fetch(latest, '(RFC822)')
        return_msg = em.message_from_bytes(msg_data[0][1])
        return return_msg

    def parse_message(self, message):
        if message.is_multipart():
            for part in message.walk():
                part_type = part.get_content_type()
                part_dispo = str(part.get('Content-Disposition'))

                if part_type == 'text/plain' and 'attachment' not in part_dispo:
                    body = part.get_payload(decode=False)
                    break
        else:
            body = message.get_payload(decode=False)
        print(type(body))
        print(body)
        return body

