from wtforms import Form, BooleanField, RadioField, StringField, PasswordField, validators, IntegerField, Field
from flask import Flask
from wtforms.fields.html5 import EmailField

# flask_app = Flask(__name__)
# flask_app.config.from_pyfile("settings.py")


class RegistrationForm(Form):
    email = EmailField('Email (username)', [validators.Length(min=6, max=50),
                                            validators.DataRequired(),
                                            validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    name = StringField('name', [validators.Length(min=1, max=100),
                                validators.DataRequired()])
    gender = RadioField('Gender', [validators.DataRequired()],
                        choices=[("male", "Male"),
                                 ("female", "Female"),
                                 ("other", "Other"),
                                 ("unknown", "I'd rather not say")])
    age = IntegerField('Age', [validators.Optional(),
                               validators.NumberRange(
                                   min=13, message="Must be at least 13 to use this application."
                               )])
    tos = BooleanField(' I understand and agree to the Terms of Service', [validators.DataRequired()])



class Options:
    def __init__(self, q, max_results):
        self.q = q
        self.max_results = max_results

# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash("You need to login first")
#             return redirect(url_for('login_page'))
#
#     return wrap