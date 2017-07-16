import pymongo
from pymongo import MongoClient
from mongoengine import *

client = MongoClient('localhost',27017)

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


