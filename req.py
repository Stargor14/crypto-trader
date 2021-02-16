import requests
import json
from binance.client import Client
import datetime

with open('Z:\github/keys.json') as f:
  data = json.load(f)

apikey = data['public']
secretkey = data['secret']

global client
client = Client(apikey, secretkey)
global ms
epoch = datetime.datetime.utcfromtimestamp(0)
ms = (datetime.datetime.now() - epoch).total_seconds() * 1000.0
global prices
prices = []

def run():
    global prices
    def reqold():
        global client
        global prices
        global ms
        backtime = ms-86400000*int(input("Start days ago: "))
        forwardtime = ms-86400000*int(input("End days ago: "))
        klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE,str(backtime),str(forwardtime))
        a = []
        for i in klines:
            a.append({"open":float(i[1]), "close":float(i[4]),"low":float(i[3]), "high":float(i[2])})
        print("Started!")
        return a
    prices=reqold()
