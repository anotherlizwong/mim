from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField
from flask import Flask

# flask_app = Flask(__name__)
# flask_app.config.from_pyfile("settings.py")


class RegistrationForm(Form):
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirm')
    accept_tos = BooleanField('tos', [validators.DataRequired()])
    name = StringField('name', [validators.Length(min=1, max=100), validators.DataRequired()])
    gender = StringField('gender', [validators.DataRequired()])
    age = IntegerField('age', [validators.Optional(),
                               validators.NumberRange(
                                   13,150000, message="Must be at least 13 to use this application."
                               )])



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