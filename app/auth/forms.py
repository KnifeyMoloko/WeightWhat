from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 128), Email()],
                        id="login-email",
                        render_kw={"placeholder": "Enter your email"})
    pswrd = PasswordField("Password", validators=[DataRequired(), Length(1, 128)],
                          id="login-pass",
                          render_kw={"placeholder": "Enter your password"})
    keep_me = BooleanField('Keep me signed in', id="login-keep")
    submit = SubmitField("Sign in", id="login-submit")


class RegisterForm(FlaskForm):
    username = StringField("User name", validators=[DataRequired(),
                                                    Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                                           message='user names must only '
                                                                   'have letters, numbers or underscores'),
                                                    Length(1, 128)])
    email = StringField("User email", validators=[DataRequired(),
                                                  Length(1, 128),
                                                  Email()])
    password = PasswordField("User password", validators=[DataRequired(),
                                                          Length(min=4, max=128, message="Please enter password"),
                                                          EqualTo('password_confirmation',
                                                                  message="Password and password confirmation"
                                                                          " don't match.")])
    password_confirmation = PasswordField("Confirm password: ",
                                          validators=[DataRequired(),
                                                      Length(min=4,
                                                             max=128,
                                                             message="Please enter password")]
                                          )
    submit = SubmitField("Register")
