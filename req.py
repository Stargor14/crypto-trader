import requests
import json
import time
from binance.client import Client

with open('Z:\github\keys.json') as f:
  data = json.load(f)

apikey = data['public']
secretkey = data['secret']
global client
client = Client(apikey, secretkey)

global hlength
hlength = 100
global prices
prices = []

def run():
    global prices
    global runs
    def runinit():
        global client
        global hlength
        klines = client.futures_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=hlength)
        a = []
        for i in klines:
            a.append({"time":i[0], "open":float(i[1]), "close":float(i[4]),"low":float(i[3]), "high":float(i[2])})
        return a
    def reqc():
        global client
        try:
            kline = client.futures_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=1)
            return {"time":kline[0][0], "open":float(kline[0][1]), "close":float(kline[0][4]),"low":float(kline[0][4]), "high":float(kline[0][4])}
        except:
            return prices[0]
    if len(prices)==0:
        prices=list(reversed(runinit()))
    if len(prices)==hlength:
        if prices[0]['time'] != reqc()['time']:
            prices.pop(hlength-1)
            prices.insert(0,reqc())
        else:
            prices[0] = reqc()
    time.sleep(1)
