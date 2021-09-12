from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, URL, Email


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    number = TelField("Phone Number", validators=[InputRequired()])
