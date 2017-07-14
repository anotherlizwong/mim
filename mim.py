from flask import Flask, redirect, render_template, request, session, flash, url_for
from flask.ext.bcrypt import Bcrypt
from flask.ext.csrf import csrf
import mim.mendeley_api
import mim.youtube_api
import mim.core as core
from mim.models import *

app = Flask(__name__)
app.config.from_object('settings')
bcrypt = Bcrypt(app)
csrf(app)

@app.route('/')
def index():
    if 'token' in session:
        return redirect('/listDocuments')

    auth = mim.mendeley_api.mendeley.start_authorization_code_flow()

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


@app.route('/listDocuments')
def list_documents():
    if 'token' not in session:
        return redirect('/')

    mendeley_session = mim.mendeley_api.get_session_from_cookies()

    name = mendeley_session.profiles.me.display_name
    docs = mendeley_session.documents.list(view='client').items

    return render_template('library.html', name=name, docs=docs)


@app.route('/document')
def get_document():
    if 'token' not in session:
        return redirect('/')

    mendeley_session = mim.mendeley_api.get_session_from_cookies()

    document_id = request.args.get('document_id')
    doc = mendeley_session.documents.get(document_id)

    return render_template('metadata.html', doc=doc)


@app.route('/metadataLookup')
def metadata_lookup():
    if 'token' not in session:
        return redirect('/')

    mendeley_session = mim.mendeley_api.get_session_from_cookies()

    doi = request.args.get('doi')
    doc = mendeley_session.catalog.by_identifier(doi=doi)

    return render_template('metadata.html', doc=doc)


@app.route('/download')
def download():
    if 'token' not in session:
        return redirect('/')

    mendeley_session = mim.mendeley_api.get_session_from_cookies()

    document_id = request.args.get('document_id')
    doc = mendeley_session.documents.get(document_id)
    doc_file = doc.files.list().items[0]

    return redirect(doc_file.download_url)


@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            this_user = User.objects.get(email=request.form['username'])
            if request.form['username'] != this_user.email:
                error = 'Invalid username'
            elif bcrypt.check_password_hash(this_user.password, request.form['password']) == False:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['this_user'] = {'first_name':this_user.first_name}

                flash('You were logged in')
                return redirect(url_for('index'))
        except:
            flash('User does not exist')
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run()
