import os
import util
import Recommender as rec

from mendeley import Mendeley
from mendeley.session import MendeleySession


if 'MENDELEY_ID' in os.environ:
    MENDELEY_APP_ID, MENDELEY_KEY = os.environ['MENDELEY_ID'], os.environ['MENDELEY_SECRET']
else:
    MENDELEY_APP_ID, MENDELEY_KEY = util.secretkey_config("mendeley")
REDIRECT_URI = 'http://localhost:5000/oauth'

mendeley = Mendeley(MENDELEY_APP_ID, MENDELEY_KEY, REDIRECT_URI)
session = mendeley.start_client_credentials_flow().authenticate()


def get_session_from_cookies():
    return MendeleySession(mendeley, session['token'])


def get_one(options):
    documents, page = search(options)

    # ensure unique results based on user history
    documents = util.get_unique(documents)
    if len(documents) > 0:
        one_document = rec.pick_option(documents)
    else:
        # if there aren't any unique documents, go to the next page of search results
        options.pageToken = page.next_page
        if options.pageToken is None:
            return None  # if it's the last page of the search, stop
        else:
            return get_one(options)

    return one_document


def search(options):
    if options.pageToken is None:
        search_results = session.catalog.search(
            query=options.q,
            view="client"
        ).list(page_size=options.max_results)
    else:
        search_results = options.pageToken

    docs = []
    for doc in search_results.items:
        docs.append(format_results(doc))

    return docs, search_results


def format_results(doc):
    document = {"content_type": "paper",
                "id": doc.id,
                "title": doc.title,
                "author": {"name": doc.source},
                "authors": doc.authors,
                "description": doc.abstract,
                "date": doc.year,
                "url": find_actual_doc_url(doc)
                }

    return document


def example():
    options = util.Options("Educational Technology", 25)

    try:
        print search(options)
    except Exception, e:
        print "An error occurred:\n%s" % e.message


def find_actual_doc_url(doc):
    url = doc.link
    if doc.source is not None and doc.year is not None:
        query_terms = "\"" + doc.title + "\"" + " " + doc.source + " " + str(doc.year)
        if doc.identifiers is not None and "isbn" in doc.identifiers:
            query_terms += " isbn:"+doc.identifiers["isbn"]
        query_terms = query_terms.replace(" ", "%20")
        google_lucky = "http://www.google.com/search?q="+query_terms+"&btnI"
        url = google_lucky
    return url

# example()