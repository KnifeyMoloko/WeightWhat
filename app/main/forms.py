from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime


class LoginForm(FlaskForm):
    user = StringField("User login: ", validators=[DataRequired()])
    pswrd = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    username = StringField("User name: ", validators=[Email("Enter valid e-mail address"),
                                                      DataRequired()])
    password = PasswordField("User password: ",
                             validators=[DataRequired(),
                                         Length(min=4,
                                                max=128,
                                                message="Please enter password")])
    password_confirmation = PasswordField("Confirm password: ",
                                          validators=[DataRequired(),
                                                      Length(min=4,
                                                             max=128,
                                                             message="Please enter password")]
                                          )
    submit = SubmitField("Submit")


class DateForm(FlaskForm):
    today = datetime.today()
    d = DateField("Choose a date", id='dp', default=today)
    submit = SubmitField("Submit")
