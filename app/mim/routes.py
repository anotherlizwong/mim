from flask import Flask, redirect, render_template, request, session, flash, url_for
from flask.ext.bcrypt import Bcrypt
from flask.ext.csrf import csrf

from app.mim import RegistrationForm
from models import *

import core
import mendeley_api
import app.mim.helpers as util
# from app.mim import flask_app

flask_app = Flask(__name__)
flask_app.config.from_pyfile("settings.py")

bcrypt = Bcrypt(flask_app)
csrf(flask_app)


@flask_app.route('/home')
def index():
    if 'token' in session:
        return redirect('/history')

    auth = mendeley_api.mendeley.start_authorization_code_flow()

    rec = core.get_random()
    name = "friend"

    return render_template('index.html',
                           rec=rec,
                           name=name)

# @app.route('/oauth')
# def auth_return():
#     auth = mim.mendeley_api.mendeley.start_authorization_code_flow(state=session['state'])
#     mendeley_session = auth.authenticate(request.url)
#
#     session.clear()
#     session['token'] = mendeley_session.token
#
#     return redirect('/listDocuments')


@flask_app.route('/history')
def list_documents():
    if 'token' not in session:
        return redirect('/home')

    mendeley_session = mendeley_api.get_session_from_cookies()

    name = mendeley_session.profiles.me.display_name
    docs = mendeley_session.documents.list(view='client').items

    return render_template('history.html', name=name, docs=docs)


@flask_app.route('/document')
def get_document():
    if 'token' not in session:
        return redirect('/home')

    mendeley_session = mendeley_api.get_session_from_cookies()

    document_id = request.args.get('document_id')
    doc = mendeley_session.documents.get(document_id)

    return render_template('metadata.html', doc=doc)


@flask_app.route('/search')
def metadata_lookup():
    if 'token' not in session:
        return redirect('/home')

    mendeley_session = mendeley_api.get_session_from_cookies()

    doi = request.args.get('doi')
    doc = mendeley_session.catalog.by_identifier(doi=doi)

    return render_template('history.html', doc=doc)


@flask_app.route('/download')
def download():
    if 'token' not in session:
        return redirect('/home')

    mendeley_session = mendeley_api.get_session_from_cookies()

    document_id = request.args.get('document_id')
    doc = mendeley_session.documents.get(document_id)
    doc_file = doc.files.list().items[0]

    return redirect(doc_file.download_url)


@flask_app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect('/home')


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            # this_user = User.objects.get(email=request.form['username'])
            this_user = users.find_one({'email': request.form['email']})
            if request.form['email'] != this_user.email:
                error = 'Invalid username'
            elif bcrypt.check_password_hash(this_user.password, request.form['password']) is False:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['username'] = this_user.email
                session['this_user'] = this_user.name

                flash('Logging in...')
                return redirect(url_for('index'))
        except:
            flash('User does not exist')
    return render_template('login.html', error=error)


@flask_app.route('/register', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            email = form.email.data
            name = form.name.data
            gender = form.gender.data
            year_of_birth = util.get_year(form.age)
            password = bcrypt.hashpw(str(form.password.data), bcrypt.gensalt())

            # check username for duplicate
            result = users.insert_one(
                {
                    "email":    email,
                    "password": password,
                    "name":     name,
                    "gender":   gender,
                    "yob":      year_of_birth,
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

                return redirect(url_for('/login'))

        return render_template("register.html", form=form)

    except Exception as e:
        return (str(e))


@flask_app.route("/logout")
# @login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('/login'))


# can leave this in probably...
if __name__ == '__main__':
    flask_app.run(debug=True)