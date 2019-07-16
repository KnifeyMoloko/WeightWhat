"""Unit tests for profile_settings section of WeightWhat app."""

import unittest
from sqlalchemy_utils import database_exists, create_database
from app import create_app, db, mail, email
from app.db_models import User

class ProfileSettingsTestCases(unittest.TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

