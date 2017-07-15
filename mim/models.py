import pymongo
from pymongo import MongoClient
from mongoengine import *

client = MongoClient('localhost',27017)

# get the sampleDB database

db = client.mim
resources = db.resources
users = db.users
user_history = db.user_history


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    password = StringField(max_length=200)


class History(Document):
    user = StringField(required=True)
    opinion = IntField(required=True)
    rec_id = ObjectIdField()


