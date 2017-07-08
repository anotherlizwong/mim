import helpers
from mendeley import Mendeley
from mendeley.session import MendeleySession

MENDELEY_KEY = helpers.secretkey_config("mendeley")
REDIRECT_URI = 'http://localhost:5000/oauth'

mendeley = Mendeley("4546", MENDELEY_KEY, REDIRECT_URI)
session = mendeley.start_client_credentials_flow().authenticate()


def get_session_from_cookies():
    return MendeleySession(mendeley, session['token'])


def mendeley_search(options):
    search_results = session.catalog.search(
        query=options.q,
        view="client"
    ).list(page_size=options.max_results).items

    docs = []
    for doc in search_results:
        docs.append(format_results(doc))

    return docs


def format_results(doc):
    doc.description = doc.abstract
    if len(doc.abstract) > helpers.DESCRIPTION_LIMIT:
        doc.description = doc.abstract[:helpers.DESCRIPTION_LIMIT]+"..."

    document = {"title": doc.title,
                "author": doc.source,
                "authors": doc.authors,
                "display_description": doc.description,
                "description": doc.abstract,
                "date": doc.year,
                "url": doc.link,
                }

    return document


def example():
    options = helpers.Options("Educational Technology", 25)

    # try:
    print mendeley_search(options)
    # except Exception, e:
    #     print "An error occurred:\n%s" % e.message


example()