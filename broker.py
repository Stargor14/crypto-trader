import requests
import json
from binance.client import Client

with open('Z:\github/keys.json') as f:
  data = json.load(f)

apikey = data['public']
secretkey = data['secret']

client = Client(apikey, secretkey)
global profit
profit = 0
global tradesum
tradesum = 0
def long(en):
    print(f"Entered LONG at: {en}")
    #long function
def short(en):
    print(f"Entered SHORT at: {en}")
    #short function
def close(ex,pnl):
    global profit
    global tradesum
    tradesum +=1
    profit+=pnl-.08
    print(f"CLOSED at: {ex} with pNl of: {pnl-.08}")
    print(f"Total pNl: {profit} Total trades: {tradesum}")
