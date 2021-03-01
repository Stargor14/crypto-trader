import json
from binance.client import Client

with open('keys.json','r') as r:
    data  = json.load(r)
    api_key = data['public']
    api_secret = data['secret']

client = Client(api_key, api_secret)
