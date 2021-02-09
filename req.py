import requests
import json
import time

prices = []

def req31():
    prices31 = []
    r = requests.get("https://api.coindesk.com/v1/bpi/historical/close.json")
    j = json.loads(r.text)
    for i in j['bpi']:
        prices31.append(j['bpi'][i])
    print(prices31)
def run(t):
    def reqc():
        r = requests.get("https://api.binance.com/api/v3/ticker/price")
        j = json.loads(r.text)
        return j[11]['price']
    if len(prices)==60:
        prices.pop(19)
        prices.insert(0,float(reqc()))
    if len(prices)!=60:
        prices.insert(0,float(reqc()))
        print(len(prices))
    time.sleep(t)

    
