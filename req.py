import json
import datetime
from binance.client import Client

with open('keys.json','r') as r:
    data  = json.load(r)
    api_key = data['public']
    api_secret = data['secret']

global client
client = Client(api_key, api_secret)

class Prices:
    def __init__(self,prices,interval):
        self.prices = prices
        self.interval = interval
global pair
pair = "BTCUSDT"
def live_request(interval):
    global client
    global pair
    #requests last 500 candles by default
    epoch = datetime.datetime.utcfromtimestamp(0)
    ms = (datetime.datetime.utcnow() - epoch).total_seconds() * 1000.0
    startTime = ms - 3600000
    candles = client.get_historical_klines(pair, interval,str(startTime))
    a = []
    for i in candles:
        a.append({"open":float(i[1]), "close":float(i[4]),"low":float(i[3]), "high":float(i[2])})
    return a

def past_request(interval,backtime,forwardtime):
    global client
    global pair
    #determines current time in milliseconds, subtracts x amount of millsecods away and starts there
    klines = client.get_historical_klines(pair, interval, str(backtime),str(forwardtime))
    a = []
    for i in klines:
        a.append({"time":i[0], "open":float(i[1]), "close":float(i[4]),"low":float(i[3]), "high":float(i[2])})
    return a
