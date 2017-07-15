from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("settings.py")


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.DataRequired()])


class Options:
    def __init__(self, q, max_results):
        self.q = q
        self.max_results = max_results