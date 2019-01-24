from WeightWhat import db


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True, index=True)
    value = db.Column(db.Float)
    user_id = db.relationship("User", backref="measurement_id")

    def __repr__(self):
        return '<Measurement is %d>' % self.value


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    user_pswrd = db.Column(db.Integer, db.ForeignKey('login_data.pswrd'))
    measurement_id = db.Column(db.Integer, db.ForeignKey('measurements.id'))

    def __repr__(self):
        return "<User is %r>" % self.value


class LoginData(db.Model):
    __tablename__ = 'login_data'
    id = db.Column(db.Integer, primary_key=index)
    pswrd = db.Column(db.Integer)
    user = db.relationship('User', backref='loginData')

    def __repr__(self):
        return "LoginData is %r" % self.pswrd
