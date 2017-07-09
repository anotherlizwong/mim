from flask import Flask, redirect, render_template, request, session
import mim.mendeley_api
import mim.youtube_api

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    if 'token' in session:
        return redirect('/listDocuments')

    auth = mim.mendeley_api.mendeley.start_authorization_code_flow()
    session['state'] = auth.state

    name = "friend"
    content_type = "video"
    time_estimate = "(13:50)"
    url = "http://127.0.0.1"
    thumbnail_url = "http://24.media.tumblr.com/c2e147bcdf9901b8296b53e94ffa72fe/tumblr_muh0fiUCCJ1sdauago1_500.gif"
    thumbnail_width = 498
    thumbnail_height = 376.5
    display_description = "Test"

    return render_template('index.html',
                           name=name,
                           content_type=content_type,
                           time_estimate=time_estimate,
                           url=url,
                           thumbnail_url=thumbnail_url,
                           thumbnail_width=thumbnail_width,
                           thumbnail_height=thumbnail_height,
                           display_description=display_description)


@app.route('/oauth')
def auth_return():
    auth = mim.mendeley_api.mendeley.start_authorization_code_flow(state=session['state'])
    mendeley_session = auth.authenticate(request.url)

    session.clear()
    session['token'] = mendeley_session.token

    return redirect('/listDocuments')


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


if __name__ == '__main__':
    app.run()
