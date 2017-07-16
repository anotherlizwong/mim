import random
from app.mim import Options
import mendeley_api as mendeley
import youtube_api as youtube

DESCRIPTION_LIMIT = 100
MODULES = [youtube, mendeley]


class Content():
    def __init__(self):
        self.content_type = "video"
        self.title = "sample title"
        self.author = {"url": "", "name": "James"}
        self.time_estimate = "(00:00)"
        self.url = "http://127.0.0.1"
        self.thumbnail_url = "http://24.media.tumblr.com/c2e147bcdf9901b8296b53e94ffa72fe/tumblr_muh0fiUCCJ1sdauago1_500.gif"
        self.thumbnail_width = 498
        self.thumbnail_height = 376.5
        self.description = "Bulbasaur Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ivysaur Lorem ipsum dolor sit amet, consectetur adipiscing elit. Venusaur Lorem ipsum dolor sit amet, consectetur adipiscing elit. Charmander Lorem ipsum dolor sit amet, consectetur adipiscing elit. Charmeleon Lorem ipsum dolor sit amet, consectetur adipiscing elit. Charizard Lorem ipsum dolor sit amet, consectetur adipiscing elit. Squirtle Lorem ipsum dolor sit amet, consectetur adipiscing elit. Wartortle Lorem ipsum dolor sit amet, consectetur adipiscing elit. Blastoise Lorem ipsum dolor sit amet, consectetur adipiscing elit. Caterpie Lorem ipsum dolor sit amet, consectetur adipiscing elit. Metapod Lorem ipsum dolor sit amet, consectetur adipiscing elit. Butterfree Lorem ipsum dolor sit amet, consectetur adipiscing elit. Weedle Lorem ipsum dolor sit amet, consectetur adipiscing elit. Kakuna Lorem ipsum dolor sit amet, consectetur adipiscing elit. Beedrill Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pidgey Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pidgeotto Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pidgeot Lorem ipsum dolor sit amet, consectetur adipiscing elit. Rattata Lorem ipsum dolor sit amet, consectetur adipiscing elit. Raticate Lorem ipsum dolor sit amet, consectetur adipiscing elit. Spearow Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fearow Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ekans Lorem ipsum dolor sit amet, consectetur adipiscing elit. Arbok Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pikachu Lorem ipsum dolor sit amet, consectetur adipiscing elit. Raichu Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sandshrew Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sandslash Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nidoran Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nidorina Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nidoqueen Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nidoran Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nidorino Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nidoking Lorem ipsum dolor sit amet, consectetur adipiscing elit. Clefairy Lorem ipsum dolor sit amet, consectetur adipiscing elit. Clefable Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vulpix Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ninetales Lorem ipsum dolor sit amet, consectetur adipiscing elit. Jigglypuff Lorem ipsum dolor sit amet, consectetur adipiscing elit. Wigglytuff Lorem ipsum dolor sit amet, consectetur adipiscing elit. Zubat Lorem ipsum dolor sit amet, consectetur adipiscing elit. Golbat Lorem ipsum dolor sit amet, consectetur adipiscing elit. Oddish Lorem ipsum dolor sit amet, consectetur adipiscing elit. Gloom Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vileplume Lorem ipsum dolor sit amet, consectetur adipiscing elit. Paras Lorem ipsum dolor sit amet, consectetur adipiscing elit."


    def set(self, content_type, title, author, time_estimate, url, thumbnail_url, thumbnail_width, thumbnail_height, description):
        self.content_type = content_type
        self.title = title
        self.author = author
        self.time_estimate = time_estimate
        self.url = url
        self.thumbnail_url = thumbnail_url
        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height
        self.description = description

    def build(self, from_engine):
        self.content_type = from_engine["content_type"]
        self.title = from_engine["title"]
        if "name" in self.author:
            self.author = from_engine["authors"]
        else:
            self.author.name = from_engine["author"]
        self.url = from_engine["url"]
        self.description = from_engine["description"]
        if "thumbnail" in from_engine:
            self.thumbnail_url = from_engine["thumbnail"]["url"]
            self.thumbnail_height = from_engine["thumbnail"]["height"]
            self.thumbnail_width = from_engine["thumbnail"]["width"]

def get_random():
    engine = MODULES[random.randint(0,len(MODULES)-1)]
    search_results = engine.search(Options("Educational Technology", 25))
    recommendation = search_results[random.randint(0,len(search_results)-1)]
    selection = Content()
    selection.build(recommendation)
    return selection



