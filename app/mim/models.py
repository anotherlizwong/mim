import pymongo
import os
from pymongo import MongoClient
from mongoengine import *

# client = MongoClient('localhost',27017)
if "pw" in os.environ:
    pw = os.environ["pw"]
    database = os.environ["db"]
    client = pymongo.MongoClient("mongodb://obgynbbq-admin:" +
                             pw +
                             "@mimcluster-shard-00-00-mba0j.mongodb.net:27017," +
                             "mimcluster-shard-00-01-mba0j.mongodb.net:27017," +
                             "mimcluster-shard-00-02-mba0j.mongodb.net:27017/" +
                             database +
                             "?ssl=true&replicaSet=MimCluster-shard-0&authSource=admin")
else:
    client = MongoClient('localhost', 27017)

# get the sampleDB database

db = client.mim
resources = db.resources
users = db.users
users.create_index([('email', pymongo.ASCENDING)], unique=True)
user_history = db.user_history


class User(Document):
    email = StringField(required=True, unique=True)
    password = StringField(max_length=200)
    name = StringField(max_length=100)
    gender = StringField(max_length=20)
    yob = IntField()


class History(Document):
    user = StringField(required=True)
    opinion = IntField(required=True)
    rec_id = ObjectIdField()


def already_seen(user, docId):
    if user_history.find({
        "user": user,
        "content": {"id": docId}
    }).limit(1).count() > 0:
        return True
    else:
        return False


def get_user_history(user):
    return user_history.find({"user": user})