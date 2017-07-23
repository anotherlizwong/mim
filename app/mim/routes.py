import os
import random
import core
import mendeley_api
import util
from flask import Flask, redirect, render_template, request, session, flash, url_for
from flask_bcrypt import Bcrypt
from pymongo.errors import DuplicateKeyError
from models import *
from . import RegistrationForm
from . import logger


flask_app = Flask(__name__)
if 'SECRET_KEY' in os.environ:
    flask_app.secret_key = os.environ['SECRET_KEY']
else:
    flask_app.secret_key = "LOCAL"

bcrypt = Bcrypt(flask_app)
# csrf(flask_app)


@flask_app.route('/')
def index():
    if 'token' not in session:
        return redirect(url_for('login'))

    rec = core.get_random("Educational Technology")
    historical_data = core.get_history(session["email"])
    name = session.get("name", "friend")
    classes = {
        "interesting": "button-primary",
        "uninteresting": "",
        "next": ""
    }

    return render_template('index.html',
                           rec=rec,
                           name=name,
                           classes=classes,
                           history=historical_data)

@flask_app.route('/record', methods=['GET', 'POST'])
def record():
    try:
        if request.method == "POST":
            doc = {
                "id": request.form["id"],
                "url": request.form["url"],
                "content_type": request.form["type"],
                "title": request.form["title"],
            }
            opinion = {
                "opinion": util.get_opinion_value(request.form["opinion"]),
                "rec_id": request.form["id"]
            }
            try:
                user_history.insert({
                    "user": session["email"],
                    "content": doc,
                    "opinion": opinion})
            except Exception, e:
                flash(e.message)

            if opinion["opinion"] is not 0:
                flash("Thanks for your feedback!", "feedback")

            try:
                if "tokens" in os.environ:
                    token_no = str(random.randint(1,8))
                    flash(os.environ["token"+token_no],"token")
            except:
                logger.error("Could not get token.", exc_info=True)

    except:
        flash("Something went wrong and we couldn't record your response.", "error")
        logger.error("Could not record opinion.", exc_info=True)

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
            elif bcrypt.check_password_hash(this_user["password"], request.form['password']) is False:
                error = 'Invalid password'
            else:
                session["logged_in"] = True
                session["token"] = util.generate_key()
                session["email"] = this_user["email"]
                session["name"] = this_user["name"]

                flash("Logged in!")
                return redirect(url_for('index'))
        except Exception as e:
            flash("That's not quite right. Try that username and password one more time?", "error")
            logger.warn("Could log in user.", exc_info=True)

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
            password = bcrypt.generate_password_hash(str(form.password.data), 10)
            name = form.name.data.capitalize()
            gender = form.gender.data
            year_of_birth = util.get_year(form.age.data)
            tos_check_date = util.get_today()

            # check username for duplicate
            try:
                result = users.insert_one(
                    {
                        "email":    email,
                        "password": password,
                        "name":     name,
                        "gender":   gender,
                        "yob":      year_of_birth,
                        "tos":      tos_check_date
                    }
                )
            except DuplicateKeyError, e:
                flash("That username is already taken, please choose another.", "error")
                return render_template('register.html', form=form)

            # No exception is good...
            flash("Thanks for registering!")

            session['logged_in'] = True
            session["token"] = util.generate_key()
            session['username'] = email
            session['name'] = name

            return redirect(url_for('index'))

    except Exception as e:
        flash(e.message, "error")
        logger.error("Issue with registering user.", exc_info=True)

    return render_template('register.html', form=form)


# While the data model is in flux, it's helpful to have a quick dump method
if "data_purge" in os.environ:
    secret_route = os.environ["data_purge"]
else:
    secret_route = "/dumpData"


@flask_app.route(secret_route)
def purge_data():
    try:
        logger.warn("Dumping user history data.")
        user_history.remove({})
        flash("All user history data purged.","error")
    except:
        logger.error("Could not dump user history data.", exc_info=True)
    return redirect(url_for('index'))
