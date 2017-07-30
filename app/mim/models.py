import pymongo
import os
import json
from pymongo import MongoClient
from mongoengine import *
from bson.json_util import dumps

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


def already_seen(user, doc_id):
    existing = get_user_history(user)
    for item in existing:
        if item["content"]["id"] == doc_id:
            return True
    return False


def get_user_history(user=None, as_json=False):
    """
    Get user history of a single user or all users
    Can be returned as json for consumption by a recommender or a mongodb document
    :param user: Optional String, would be username if supplied
    :param as_json: Optional Boolean, defaulted to False
    :return: Either a mongodb document or a json string
    """
    if user is not None:
        user = {"user": user}
    else:
        user = {}

    doc = user_history.find(user)

    if as_json:
        return dumps(doc)
    else:
        return doc
