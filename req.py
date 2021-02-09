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
        r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        j = json.loads(r.text)
        return j['bpi']['USD']['rate_float']   
    if len(prices)==14:
        prices.pop(13)
        prices.insert(0,reqc())
    if len(prices)!=14:
        prices.insert(0,reqc())
        print(len(prices))
    time.sleep(t)
    
