import requests
import json
import time

hlength = 0
prices = []

def run(t):
    def reqc():
        r = requests.get("https://api.binance.com/api/v3/ticker/price")
        j = json.loads(r.text)
        return j[11]['price']

    if len(prices)==hlength:
        prices.pop(hlength-1)
        prices.insert(0,float(reqc()))
    if len(prices)!=hlength:
        prices.insert(0,float(reqc()))
        print(len(prices))

    time.sleep(t)
