from flask import current_app

from . import db, login_mgmt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_mgmt.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))  # return the User object or None


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True, index=True)
    value = db.Column(db.Float)
    user_id =db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Measurement is %d>' % self.value


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String, index=True)
    user_pswrd = db.Column(db.String(128))
    user_confirmed = db.Column(db.Boolean, default=False)
    measurements = db.relationship("Measurement", backref='user', lazy="dynamic")

    def __repr__(self):
        return "<User is %r>" % self.value

    @property
    def password(self):
        raise AttributeError('This is not a readable attribute')

    @password.setter
    def password(self, password):
        self.user_pswrd = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_pswrd, password)

    def create_auth_token(self, timeout=3600):
        # create auth token for self.id with SECRET_KEY with a defined timeout
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=timeout)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def validate_auth_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        # check if the token is even a loadable itsdangerous object
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        # compare the confirm value with self.id
        if data.get('confirm') != self.id:
            return False

        self.user_confirmed = True
        db.session.add(self)
        return True
