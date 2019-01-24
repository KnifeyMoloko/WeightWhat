from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, DateField
from wtforms.validators import DataRequired
from datetime import datetime


class LoginForm(FlaskForm):
    user = StringField("User login: ", validators=[DataRequired()])
    pswrd = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DateForm(FlaskForm):
    today = datetime.today()
    d = DateField("Choose a date", id='dp', default=today)
    submit = SubmitField("Submit")
