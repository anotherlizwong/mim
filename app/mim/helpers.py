import json


def secretkey_config(api):
    json_data = open("./app/mim/client_secrets.json").read()
    data = json.loads(json_data)
    return data[api]["client_id"], data[api]["client_secret"]



