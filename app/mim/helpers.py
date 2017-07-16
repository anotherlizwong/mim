import json
import datetime

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
