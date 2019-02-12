from . import db, login_mgmt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_mgmt.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))  # return the User object or None


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True, index=True)
    value = db.Column(db.Float)
    user_id = db.relationship("User", backref="measurement")

    def __repr__(self):
        return '<Measurement is %d>' % self.value


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String, index=True)
    user_pswrd = db.Column(db.String(128))
    measurement_id = db.Column(db.Integer, db.ForeignKey('measurements.id'))

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

