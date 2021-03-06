import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = "[WeightWhatApp] "
    MAIL_SENDER = 'WeighWhatApp Admin <weightwhatadmin@example.com>'
    APP_ADMIN = os.environ.get('APP_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = 'smtp.googlemail.com'
    MAIL_SUBJECT_PREFIX = "[WeightWhatAppTesting] "
    MAIL_SENDER = 'WeighWhatApp Testing <weightwhatadmin@example.com>'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///'


class TestingWithEmail(Config):
    TESTING = False  # this is to allow flask-mail to actually send emails
    SERVER_NAME = 'smtp.googlemail.com'
    MAIL_SUBJECT_PREFIX = "[WeightWhatAppTesting] "
    MAIL_SENDER = 'WeighWhatApp Testing <weightwhatadmin@example.com>'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-prod.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'testing_with_email': TestingWithEmail,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
