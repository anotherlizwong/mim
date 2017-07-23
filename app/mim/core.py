import random

import mendeley_api as mendeley
import youtube_api as youtube
import util
from . import models
from . import Options as o
from . import Content as c

DESCRIPTION_LIMIT = 100
MODULES = [youtube, mendeley]


def get_random(keyword):
    engine = MODULES[random.randint(0, len(MODULES)-1)]
    selection = c.Content()
    selection.build(engine.get_one(o.Options(keyword, 5)))
    return selection


def get_history(username):
    history_list = models.get_user_history(username)
    history = []
    for item in history_list:
       history.append({
           "rating_class": util.get_rating_class(item["opinion"]["opinion"]),
           "rating_text": util.get_rating_text(item["opinion"]["opinion"]),
           "content_type": item["content"]["content_type"],
           "url": item["content"]["url"],
           "title": item["content"]["title"]
       })
    return reversed(history)
