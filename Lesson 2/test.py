import json
from pprint import pprint

with open("Data+scientist.json", 'r', encoding='utf-8') as f:
    text = json.load(f)
    pprint(text)