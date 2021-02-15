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

global hlength
hlength = 1000
global prices
prices = []
global runs
runs = 0
def run():
    global prices
    global runs
    def runinit():
        global client
        global hlength
        klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR,limit=1000)
        a = []
        for i in klines:
            a.append({"time":i[0], "open":float(i[1]), "close":float(i[4]),"low":float(i[3]), "high":float(i[2])})
        return a

    def reqc():
        global client
        try:
            kline = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR,limit=1)
            #8print(f"open {kline[0][1]} close {kline[0][4]}")
            return {"time":kline[0][0], "open":float(kline[0][1]), "close":float(kline[0][4]),"low":float(kline[0][4]), "high":float(kline[0][4])}
        except:
            return prices[0]
    def reqold():
        global client
        global prices
        global ms
        backtime = ms-86400000*int(input("days: "))
        klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY,str(backtime))
        a = []
        for i in klines:
            a.append({"time":i[0], "open":float(i[1]), "close":float(i[4]),"low":float(i[3]), "high":float(i[2])})
        return a
    if runs<1:
        #prices=list(reversed(reqold()))
        prices=reqold()
        runs+=1
    '''
    if len(prices)==hlength:
        if prices[0]['time'] != reqc()['time']:
            prices.pop(hlength-1)
            prices.insert(0,reqc())
            print("new candle!")
        if prices[0]['time'] == reqc()['time']:
            prices[0] = reqc()
    time.sleep(t)
    '''
