import json

DESCRIPTION_LIMIT = 100

def secretkey_config(api):
    json_data = open("./mim/client_secrets.json").read()
    data = json.loads(json_data)
    return data[api]["client_id"], data[api]["client_secret"]


class Options:
    def __init__(self, q, max_results):
        self.q = q
        self.max_results = max_results
