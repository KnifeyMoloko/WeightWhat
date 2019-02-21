from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime


class DateForm(FlaskForm):
    today = datetime.today()
    d = DateField("Choose a date", id='dp', default=today)
    submit = SubmitField("Submit")
