import os

from flask import Flask, redirect, render_template, request, session, flash, url_for
# from flask.ext.bcrypt import Bcrypt
# from flask.ext.csrf import csrf

from models import *

import core
import mendeley_api
import util
from . import RegistrationForm
# from mim import flask_app


flask_app = Flask(__name__)
if 'SECRET_KEY' in os.environ:
    flask_app.secret_key = os.environ['SECRET_KEY']
else:
    flask_app.secret_key = "LOCAL"

# bcrypt = Bcrypt(flask_app)
# csrf(flask_app)


# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash("You need to login first")
#             return redirect(url_for('login'))
#
#     return wrap


@flask_app.route('/')
def index():
    if 'token' not in session:
        return redirect(url_for('login'))

    rec = core.get_random()
    name = session.get("name", "friend")
    classes = {
        "interesting": "button-primary",
        "uninteresting": "",
        "next": ""
    }

    return render_template('index.html',
                           rec=rec,
                           name=name,
                           classes=classes)

@flask_app.route('/record', methods=['GET', 'POST'])
def record():
    try:
        if request.method == "POST":
            doc = {
                "url": request.form["recommendation"].url,
            }
            opinion = {
                "user": session["email"],
                "opinion": util.get_opinion_value(request.form["opinion"]),
                "rec_id": request.form[""]
            }
            user_history.add()

    except:
        flash("Something went wrong and we couldn't record your response.")

    return redirect(url_for('index'))


@flask_app.route('/history')
def history():
    if "token" not in session:
        return redirect(url_for('login'))

    name = session.get("name", "friend")
    docs = user_history.find({"user": session["email"]})

    return render_template('history.html', name=name, docs=docs)


@flask_app.route("/document")
def get_document():
    if "token" not in session:
        return redirect(url_for("login"))

    mendeley_session = mendeley_api.get_session_from_cookies()

    document_id = request.args.get("document_id")
    doc = mendeley_session.documents.get(document_id)

    return render_template("metadata.html", doc=doc)


@flask_app.route('/search')
def metadata_lookup():
    if 'token' not in session:
        return redirect(url_for('login'))

    mendeley_session = mendeley_api.get_session_from_cookies()

    doi = request.args.get('doi')
    doc = mendeley_session.catalog.by_identifier(doi=doi)

    return render_template("history.html", doc=doc)


@flask_app.route("/download")
def download():
    if "token" not in session:
        return redirect(url_for("login"))

    mendeley_session = mendeley_api.get_session_from_cookies()

    document_id = request.args.get("document_id")
    doc = mendeley_session.documents.get(document_id)
    doc_file = doc.files.list().items[0]

    return redirect(doc_file.download_url)


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            # this_user = User.objects.get(email=request.form['username'])
            this_user = users.find_one({"email": request.form["email"]})
            if request.form["email"] != this_user["email"]:
                error = "Invalid username."
            # elif bcrypt.check_password_hash(this_user.password, request.form['password']) is False:
            #     error = 'Invalid password'
            else:
                session["logged_in"] = True
                session["token"] = util.generate_key()
                session["email"] = this_user["email"]
                session["name"] = this_user["name"]

                flash("Logged in!")
                return redirect(url_for('index'))
        except Exception as e:
            flash(e.message + "That's not quite right. Try that username and password one more time?")
    return render_template('login.html', error=error)


# @login_required
@flask_app.route('/logout')
def logout():
    session.pop('token', None)
    session["logged_in"] = False
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('login'))


@flask_app.route('/register', methods=["GET", "POST"])
def register():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            email = form.email.data
            # password = bcrypt.hashpw(str(form.password.data), bcrypt.gensalt())
            name = form.name.data
            gender = form.gender.data
            year_of_birth = util.get_year(form.age.data)
            tos_check_date = util.get_today()

            # check username for duplicate
            result = users.insert_one(
                {
                    "email":    email,
                    # "password": password,
                    "name":     name,
                    "gender":   gender,
                    "yob":      year_of_birth,
                    "tos":      tos_check_date
                }
            )
            if result.acknowledged is False:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                flash("Thanks for registering!")

                session['logged_in'] = True
                session['username'] = email
                session['this_user'] = name

                return redirect(url_for('login'))

        return render_template("register.html", form=form)

    except Exception as e:
        return str(e)


# can leave this in probably...
if __name__ == '__main__':
    flask_app.run(debug=True)