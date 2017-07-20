import binascii
import json
import datetime
import os

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
    if opinion is "None":
        return 0
    elif opinion:
        return 1
    else:
        return -1

