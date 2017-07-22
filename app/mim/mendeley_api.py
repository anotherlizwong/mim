import os

from mendeley import Mendeley
from mendeley.session import MendeleySession

import util
import random

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
    documents = search(options)
    one_document = documents[random.randint(0, len(documents)-1)]
    return one_document


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
                "author": {"name": doc.source},
                "authors": doc.authors,
                "description": doc.abstract,
                "date": doc.year,
                "url": doc.link,
                }

    return document


def example():
    options = util.Options("Educational Technology", 25)

    try:
        print search(options)
    except Exception, e:
        print "An error occurred:\n%s" % e.message


# example()