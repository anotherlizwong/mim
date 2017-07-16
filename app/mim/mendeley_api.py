import os

from mendeley import Mendeley
from mendeley.session import MendeleySession

import helpers

MENDELEY_APP_ID, MENDELEY_KEY = os.environ['MENDELEY_ID'], os.environ['MENDELEY_SECRET'] # helpers.secretkey_config("mendeley")
REDIRECT_URI = 'http://localhost:5000/oauth'

mendeley = Mendeley(MENDELEY_APP_ID, MENDELEY_KEY, REDIRECT_URI)
session = mendeley.start_client_credentials_flow().authenticate()


def get_session_from_cookies():
    return MendeleySession(mendeley, session['token'])


def search(options):
    search_results = session.catalog.search(
        query=options.q,
        view="client"
    ).list(page_size=options.max_results).items

    docs = []
    for doc in search_results:
        docs.append(format_results(doc))

    return docs


def format_results(doc):
    document = {"content_type": "paper",
                "id": doc.id,
                "title": doc.title,
                "author": doc.source,
                "authors": doc.authors,
                "description": doc.abstract,
                "date": doc.year,
                "url": doc.link,
                }

    return document


def example():
    options = helpers.Options("Educational Technology", 25)

    try:
        print search(options)
    except Exception, e:
        print "An error occurred:\n%s" % e.message


# example()