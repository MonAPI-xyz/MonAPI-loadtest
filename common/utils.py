import json

def read_config():
    with open('config.json', 'r') as config_file:
        data = json.load(config_file)
        return data