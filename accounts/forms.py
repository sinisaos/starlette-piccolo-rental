from wtforms import Form, PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length


class RegistrationForm(Form):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=3, max=25)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=4, max=10)]
    )
    confirm = PasswordField(
        "Verify password",
        [
            InputRequired(),
            EqualTo("password", message="Passwords fields didn't match."),
        ],
    )


class LoginForm(Form):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=4, max=10)]
    )
