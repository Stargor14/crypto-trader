import requests
import json
import time
from binance.client import Client

apikey = "x15G8QtfrUCJG1F7tCahCwyCwxE7a3Mbykg8Q4Uf0Q7QKjB1B3GvCYkfzRUTS96e"
secretkey = "YyATCoS7OwFFAdaqK3UCw0zZLZoz6RWRqarMrHhGi7P08c7Muay8zDWZfV86SxA5"
global client
client = Client(apikey, secretkey)

hlength = 14
global prices
prices = []

def run(t):
    global prices
    def runinit():
        global client
        klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=hlength)
        a = []
        for i in klines:
            a.append([i[0],float(i[1]),float(i[4])])
        return a
    def reqc():
        global client
        try:
            kline = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=1)
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
