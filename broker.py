import requests
import json
from binance.client import Client

with open('Z:\github/keys.json') as f:
  data = json.load(f)

apikey = data['public']
secretkey = data['secret']

client = Client(apikey, secretkey)

def long(en):
    print(f"Entered LONG at: {en}")
def short(en):
    print(f"Entered SHORT at: {en}")
def close(ex,pnl):
    print(f"CLOSED at: {ex} with pNl of: {pnl}")
#add json recording of profits here
