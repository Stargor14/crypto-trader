import requests
import json
import time
from binance.client import Client

with open('Z:\github/keys.json') as f:
  data = json.load(f)

apikey = data['public']
secretkey = data['secret']
global client
client = Client(apikey, secretkey)

global hlength
hlength = int(input("history length: "))
global prices
prices = []

def run(t):
    global prices
    def runinit():
        global client
        global hlength
        klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=hlength)
        a = []
        for i in klines:
            a.append([i[0],float(i[1]),float(i[4])])
        #print(a)
        return a
    def reqc():
        global client
        try:
            kline = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=1)
            #8print(f"open {kline[0][1]} close {kline[0][4]}")
            return [kline[0][0], float(kline[0][1]), float(kline[0][4])]
        except:
            return prices[0]

    if len(prices)!=hlength:
        prices = runinit()

    if len(prices)==hlength:
        if prices[0][0] != reqc()[0]:
            prices.pop(hlength-1)
            prices.insert(0,reqc())
            print("new candle!")
        if prices[0][0] == reqc()[0]:
            prices[0] = reqc()
    time.sleep(t)
