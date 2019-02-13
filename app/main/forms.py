from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Length(1, 128), Email()])
    pswrd = PasswordField("Password", validators=[DataRequired()])
    keep_me = BooleanField('Keep me signed in')
    submit = SubmitField("Sign in")


class RegisterForm(FlaskForm):
    username = StringField("User name", validators=[DataRequired(),
                                                    Length(1, 128)])
    email = StringField("User email", validators=[DataRequired(),
                                                  Length(1, 128),
                                                  Email()])
    password = PasswordField("User password",
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
