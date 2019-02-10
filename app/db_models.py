from weight_what import db
from werkzeug.security import generate_password_hash, check_password_hash


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True, index=True)
    value = db.Column(db.Float)
    user_id = db.relationship("User", backref="measurement")

    def __repr__(self):
        return '<Measurement is %d>' % self.value


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
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

