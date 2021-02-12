import requests
import json
from binance.client import Client

with open('Z:\github/keys.json') as f:
  data = json.load(f)

apikey = data['public']
secretkey = data['secret']

short = 's'
long = 'l'
close = 'c'

client = Client(apikey, secretkey)

def long():
    pass
def short():
    pass
def close():
    pass
