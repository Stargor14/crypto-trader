'''

                            analysis.py              Current
                                 |                  /
        live -- broker.py -- brain.py -- requests.py
                    |            |                  \
                   past    technicals.py             Past
                          /             \
                          live          past

Within brain => press 1 or 2, 1 for live/paper 2 for backtest
'''
import anal
import broke
import req
import tech
import json
import datetime
from binance.client import Client

with open('keys.json','r') as r:
    data  = json.load(r)
    api_key = data['public']
    api_secret = data['secret']

global client
client = Client(api_key, api_secret)

def live():
    return

def paper():
    return

def backtester():
    interval = int(input("Time interval in minutes: "))
    if (interval == 1):
        interval = Client.KLINE_INTERVAL_1MINUTE
    elif (interval == 3):
        interval = Client.KLINE_INTERVAL_3MINUTE
    elif (interval == 5):
        interval = Client.KLINE_INTERVAL_5MINUTE
    elif (interval == 15):
        interval = Client.KLINE_INTERVAL_15MINUTE
    elif (interval == 30):
        interval = Client.KLINE_INTERVAL_30MINUTE
    elif (interval == 60):
        interval = Client.KLINE_INTERVAL_1HOUR
    epoch = datetime.datetime.utcfromtimestamp(0)
    ms = (datetime.datetime.now() - epoch).total_seconds() * 1000.0
    backtime = ms-86400000*int(input("Start days ago: "))
    p = req.Prices(req.past_request(interval,backtime),interval)
    macd = tech.macd(p.prices)[0]
    signal = tech.macd(p.prices)[1]
    for i in range(len(p.prices)):
        print(anal.macd.check(macd[i],signal[i]))
type = int(input("1 => live, \n2 => paper, \n3 => backtester\n"))

if (type == 1):
    live()
if (type == 2):
    paper()
if (type == 3):
    backtester()
