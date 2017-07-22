from flask import Flask
from wtforms import Form, BooleanField, RadioField, StringField, PasswordField, validators, IntegerField, Field, \
    SubmitField
from wtforms.fields.html5 import EmailField
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# flask_app = Flask(__name__)
# flask_app.config.from_pyfile("settings.py")


class RegistrationForm(Form):
    email = EmailField('Email (username)', [validators.Length(min=6, max=50),
                                            validators.DataRequired(),
                                            validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    name = StringField('Name', [validators.Length(min=1, max=100),
                                validators.DataRequired()])
    gender = RadioField('Gender', [validators.DataRequired()],
                        choices=[("male", "Male"),
                                 ("female", "Female"),
                                 ("other", "Other"),
                                 ("unknown", "I'd rather not say")],
                        default="unknown")
    age = IntegerField('Age', [validators.Optional(),
                               validators.NumberRange(
                                   min=13, message="Must be at least 13 to use this application."
                               )],
                        render_kw={"placeholder": "(optional)"})
    tos = BooleanField(' I understand and agree to the Terms of Service', [validators.DataRequired()])
    submit = SubmitField("Register")


    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True


class Options:
    def __init__(self, q, max_results):
        self.q = q
        self.max_results = max_results

