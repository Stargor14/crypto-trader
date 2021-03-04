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
import time

with open('keys.json','r') as r:
    data  = json.load(r)
    api_key = data['public']
    api_secret = data['secret']

global client
client = Client(api_key, api_secret)

def live():
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
    else:
        return

    #backtesting starts here
    b = broke.live()
    position = "closed"
    init = True
    while True:
        p = req.Prices(req.live_request(interval),interval)
        macd = tech.macd(p.prices)[0]
        signal = tech.macd(p.prices)[1]
        i = len(p.prices)-1
        stopLoss = 2
        if position == "buy":
            pnl = (p.prices[i]['close']/b.entry-1)*100
            pnlLow = (p.prices[i]['low']/b.entry-1)*100
            pnlHigh = (p.prices[i]['high']/b.entry-1)*100
        if position == "sell":
            pnl = (b.entry/p.prices[i]['close']-1)*100
            pnlLow = (b.entry/p.prices[i]['low']-1)*100
            pnlHigh = (b.entry/p.prices[i]['high']-1)*100
        if position == "closed":
            pnl = 0
            pnlLow = 0
            pnlHigh = 0
        if anal.macd.check(macd[i],signal[i],pnl,stopLoss)=="buy" and (position == "sell" or position =="closed"):
            if(position!="closed"):
                b.close(p.prices[i]['close'],"sell")
                #print(f"Closed Short, PNL {pnl} Balance: {b.balance}")
            b.enter(p.prices[i]['close'],"buy")
            position = "buy"
        if anal.macd.check(macd[i],signal[i],pnl,stopLoss)=="sell" and (position == "buy" or position =="closed"):
            if(position!="closed"):
                b.close(p.prices[i]['close'],"buy")
                #print(f"Closed Long, PNL {pnl} Balance: {b.balance}")
            b.enter(p.prices[i]['close'],"sell")
            position = "sell"
        if anal.macd.check(macd[i],signal[i],pnl,stopLoss)=="close" and position == "buy":
            b.close(b.entry*(1-(stopLoss/100)),"buy")
            #print(f"Long Stop Loss Balance: {b.balance}")
            position = "closed"
        if anal.macd.check(macd[i],signal[i],pnl,stopLoss)=="close" and position == "sell":
            b.close(b.entry*(1+(stopLoss/100)),"sell")
            #print(f"Short Stop Loss Balance: {b.balance}")
            position = "closed"
        time.sleep(1)

def paper():
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
    else:
        return

    #backtesting starts here
    b = broke.backtester()
    position = "closed"
    init = True
    while True:
        p = req.Prices(req.live_request(interval),interval)
        macd = tech.macd(p.prices)[0]
        signal = tech.macd(p.prices)[1]
        i = len(p.prices)-1
        stopLoss = 2
        if position == "buy":
            pnl = (p.prices[i]['close']/b.entry-1)*100
            pnlLow = (p.prices[i]['low']/b.entry-1)*100
            pnlHigh = (p.prices[i]['high']/b.entry-1)*100
        if position == "sell":
            pnl = (b.entry/p.prices[i]['close']-1)*100
            pnlLow = (b.entry/p.prices[i]['low']-1)*100
            pnlHigh = (b.entry/p.prices[i]['high']-1)*100
        if position == "closed":
            pnl = 0
            pnlLow = 0
            pnlHigh = 0
        if anal.macd.check(macd[i],signal[i],pnl,stopLoss)=="buy" and (position == "sell" or position =="closed"):
            if(position!="closed"):
                b.close(p.prices[i]['close'],"sell")
                print(f"Closed Short, PNL {pnl} Balance: {b.balance}")
            b.enter(p.prices[i]['close'])
            position = "buy"
        if anal.macd.check(macd[i],signal[i],pnl,stopLoss)=="sell" and (position == "buy" or position =="closed"):
            if(position!="closed"):
                b.close(p.prices[i]['close'],"buy")
                print(f"Closed Long, PNL {pnl} Balance: {b.balance}")
            b.enter(p.prices[i]['close'])
            position = "sell"
        if anal.macd.check(macd[i],signal[i],pnl,stopLoss)=="close" and position == "buy":
            b.close(b.entry*(1-(stopLoss/100)),"buy")
            print(f"Long Stop Loss Balance: {b.balance}")
            position = "closed"
        if anal.macd.check(macd[i],signal[i],pnl,stopLoss)=="close" and position == "sell":
            b.close(b.entry*(1+(stopLoss/100)),"sell")
            print(f"Short Stop Loss Balance: {b.balance}")
            position = "closed"
        print(macd[i], signal[i])
        time.sleep(1)

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
    else:
        return

    epoch = datetime.datetime.utcfromtimestamp(0)
    ms = (datetime.datetime.utcnow() - epoch).total_seconds() * 1000.0

    backtime = ms-(86400000*int(input("Start days ago: ")))
    forwardtime = backtime+(86400000*int(input("Test length: ")))

    p = req.Prices(req.past_request(interval,backtime,forwardtime),interval)
    macd = tech.macd(p.prices)[0]
    signal = tech.macd(p.prices)[1]
    strategy = int(input("strategy: 0 MACD 1 PROTOTYPE"))
    #backtesting starts here
    #macd
    if strategy == 0:
        for c in range(1,10):
            stopLoss = c
            b = broke.backtester()
            position = "closed"
            pnl = 0
            for i in range(len(p.prices)):
                if position == "buy":
                    pnl = (p.prices[i]['close']/b.entry-1)*100
                    pnlLow = (p.prices[i]['low']/b.entry-1)*100
                    pnlHigh = (p.prices[i]['high']/b.entry-1)*100
                if position == "sell":
                    pnl = (b.entry/p.prices[i]['close']-1)*100
                    pnlLow = (b.entry/p.prices[i]['low']-1)*100
                    pnlHigh = (b.entry/p.prices[i]['high']-1)*100
                if position == "closed":
                    pnl = 0
                    pnlLow = 0
                    pnlHigh = 0
                if anal.macd.check(macd[i],signal[i],pnl,stopLoss)=="buy" and (position == "sell" or position =="closed"):
                    if(position!="closed"):
                        b.close(p.prices[i]['close'],"sell")
                        #print(f"Closed Short, PNL {pnl} Balance: {b.balance}")
                    b.enter(p.prices[i]['close'])
                    position = "buy"
                if anal.macd.check(macd[i],signal[i],pnl,stopLoss)=="sell" and (position == "buy" or position =="closed"):
                    if(position!="closed"):
                        b.close(p.prices[i]['close'],"buy")
                        #print(f"Closed Long, PNL {pnl} Balance: {b.balance}")
                    b.enter(p.prices[i]['close'])
                    position = "sell"
                if anal.macd.check(macd[i],signal[i],pnlLow,stopLoss)=="close" and position == "buy":
                    b.close(b.entry*(1-(stopLoss/100)),"buy")
                    #print(f"Long Stop Loss Balance: {b.balance}")
                    position = "closed"
                if anal.macd.check(macd[i],signal[i],pnlHigh,stopLoss)=="close" and position == "sell":
                    b.close(b.entry*(1+(stopLoss/100)),"sell")
                    #print(f"Short Stop Loss Balance: {b.balance}")
                    position = "closed"
            print(f"Market: {(p.prices[-1]['close']/p.prices[0]['close']-1)*100}")
            print(f"Balance: {b.balance} Trades: {b.trades} Stop Loss: {c}%")
    #PROTOTYPE
    if strategy == 1:
        

type = int(input("1 => live, \n2 => paper, \n3 => backtester: "))

if (type == 1):
    live()
if (type == 2):
    paper()
if (type == 3):
    backtester()
