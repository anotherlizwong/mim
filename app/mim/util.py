import binascii
import json
import datetime
import os
from flask import session
from . import models


def secretkey_config(api):
    json_data = open("client_secrets.json").read()
    data = json.loads(json_data)
    return data[api]["client_id"], data[api]["client_secret"]


def get_year(age):
    if not age:
        return -1
    now = datetime.datetime.now()
    return now.year-age


def get_age(year):
    if not year:
        return
    now = datetime.datetime.now()
    return now.year-year


def get_today():
    return datetime.datetime.now()


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


def get_opinion_value(opinion):
    rating = str(opinion)
    return {
        "None": 0,
        "1": 1,
        "-1": -1
    }.get(rating, 0)


def get_unique(list):
    '''
    Check the database to see if the user already rated any items in the list.
    Remove those items from the list
    :param list:
    :return: [list with unique content, may be empty]
    '''
    unique_list = []
    user = get_user()
    for item in list:
        if not models.already_seen(user, item["id"]):
            unique_list.append(item)
    return unique_list


def get_user():
    return session["email"]


def get_rating_text(rating):
    rating = str(rating)
    return {
        "0": "No opinion",
        "1": "Liked",
        "-1": "Disliked"
    }.get(rating, "0")


def get_rating_class(rating):
    rating = str(rating)
    return {
        "0": "fa-meh-o",
        "1": "fa-thumbs-up",
        "-1": "fa-thumbs-down"
    }.get(rating, "0")
