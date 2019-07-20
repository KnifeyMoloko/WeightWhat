from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ProfileForm(FlaskForm):
        name = StringField(label="Name",
                           validators=[DataRequired(),
                                       Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                              message='User names must only have '
                                                      'letters, numbers or underscores'),
                                       Length(1, 128)],
                           id="ww-profile-name")
        email = StringField(label="Email")
        password = PasswordField(label="Password",
                                 render_kw={"placeholder": "***********",
                                            "readonly class": "form-control-plaintext"})
        submit = SubmitField(label="Submit", id="ww-profile-submit")

        def populate_placeholders(self, user):
            self.name.render_kw = {"placeholder": user.name,
                                   "readonly class": "form-control-plaintext"}
            self.email.render_kw = {"placeholder": user.email,
                                    "readonly class": "form-control-plaintext"}
