import requests
import json
import time
from binance.client import Client
import datetime

global ms
epoch = datetime.datetime.utcfromtimestamp(0)
ms = (datetime.datetime.now() - epoch).total_seconds() * 1000.0

with open('Z:\github/keys.json') as f:
  data = json.load(f)

apikey = data['public']
secretkey = data['secret']
global client
client = Client(apikey, secretkey)

global prices
prices = []
global runs
runs = 0
def run():
    global prices
    global runs

    def reqold():
        global client
        global prices
        global ms
        backtime = ms-86400000*int(input("Start days ago: "))
        forwardtime = ms-86400000*int(input("End days ago: "))
        klines = client.get_historical_klines("XRPUSDT", Client.KLINE_INTERVAL_1DAY,str(backtime),str(forwardtime))
        a = []
        for i in klines:
            a.append({"time":i[0], "open":float(i[1]), "close":float(i[4]),"low":float(i[3]), "high":float(i[2])})
        return a
    if runs<1:
        #prices=list(reversed(reqold()))
        prices=reqold()
        runs+=1
