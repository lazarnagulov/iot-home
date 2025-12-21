import json

def load_config(filePath='config.json'):
    with open(filePath, 'r') as f:
        return json.load(f)