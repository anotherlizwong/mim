import random

import mendeley_api as mendeley
import youtube_api as youtube
from . import Options as o
from . import Content as c

DESCRIPTION_LIMIT = 100
MODULES = [youtube, mendeley]


def get_random(keyword):
    engine = MODULES[random.randint(0, len(MODULES)-1)]
    selection = c.Content()
    selection.build(engine.get_one(o.Options(keyword, 5)))
    return selection




