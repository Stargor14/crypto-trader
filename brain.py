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
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score,roc_auc_score,make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
import matplotlib

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

def machine_learn():
    # ex. macd_1 = 1min MACD, macdroc1_1 = MACD ROC 1 candle 1 min
    interval = Client.KLINE_INTERVAL_1MINUTE
    p_1 = req.Prices(req.past_request(interval),interval)
    p1 = pd.DataFrame(p_1.prices)
    interval = Client.KLINE_INTERVAL_5MINUTE
    p_5 = req.Prices(req.past_request(interval),interval)
    p5 = []
    j=-1
    for i in range(len(p_1.prices)):
        if((i)%5==0):
            j+=1
        p5.append(p_5.prices[j]['close'])
        p5dict = {'close':p5}
    p5=pd.DataFrame(p5dict)
    interval = Client.KLINE_INTERVAL_15MINUTE
    p_15 = req.Prices(req.past_request(interval),interval)
    p15 = []
    j=-1
    for i in range(len(p_1.prices)):
        if((i)%15==0):
            j+=1
        p15.append(p_15.prices[j]['close'])
        p15dict = {'close':p15}
    p15=pd.DataFrame(p15dict)
    interval = Client.KLINE_INTERVAL_1HOUR
    p_60 = req.Prices(req.past_request(interval),interval)
    p60 = []
    j=-1
    for i in range(len(p_1.prices)):
        if((i)%60==0):
            j+=1
        p60.append(p_60.prices[j]['close'])
        p60dict = {'close':p60}
    p60=pd.DataFrame(p60dict)

    macd1 = tech.macd(p_1.prices)[0]
    macd5 = tech.macd(p_5.prices)[0]
    md5 = []
    j=-1
    for i in range(len(macd1)):
        if((i)%5==0):
            j+=1
        md5.append(macd5[j])
    md5dict = {'macd5':md5}
    macd5=pd.DataFrame(md5dict)

    macd15 = tech.macd(p_15.prices)[0]
    md15 = []
    j=-1
    for i in range(len(macd1)):
        if((i)%15==0):
            j+=1
        md15.append(macd15[j])
    md15dict = {'macd15':md15}
    macd15 = pd.DataFrame(md15dict)

    macd60 = tech.macd(p_60.prices)[0]
    md60 = []
    j=-1
    for i in range(len(macd1)):
        if((i)%60==0):
            j+=1
        md60.append(macd60[j])
    md60dict = {'macd60':md60}
    macd60 = pd.DataFrame(md60dict)

    signal1 = tech.macd(p_1.prices)[1]
    signal5 = tech.macd(p_5.prices)[1]
    sig5 = []
    j=-1
    for i in range(len(signal1)):
        if((i)%5==0):
            j+=1
        sig5.append(signal5[j])
    signal5dict = {'signal5':sig5}
    signal5 = pd.DataFrame(signal5dict)

    signal15 = tech.macd(p_15.prices)[1]
    sig15 = []
    j=-1
    for i in range(len(signal1)):
        if((i)%15==0):
            j+=1
        sig15.append(signal15[j])
    signal15dict = {'signal15':sig15}
    signal15 = pd.DataFrame(signal15dict)

    signal60 = tech.macd(p_60.prices)[1]
    sig60 = []
    j=-1
    for i in range(len(signal1)):
        if((i)%60==0):
            j+=1
        sig60.append(signal60[j])
    signal60dict = {'signal60':sig60}
    signal60 = pd.DataFrame(signal60dict)

    p1_change = tech.roc(p1['close'],-20)*100
    p1_roc_5 = tech.roc(p1['close'],5)*100
    p1_roc_15 = tech.roc(p1['close'],15)*100

    macd = pd.DataFrame({'macd1':macd1,'macd5':macd5['macd5'],'macd15':macd15['macd15'],'macd60':macd60['macd60']})
    signal = pd.DataFrame({'signal1':signal1,'signal5':signal5['signal5'],'signal15':signal15['signal15'],'signal60':signal60['signal60']})

    diff = pd.DataFrame({'diff1':macd['macd1']-signal['signal1'],'diff5':macd['macd5']-signal['signal5'],'diff15':macd['macd15']-signal['signal15'],'diff60':macd['macd60']-signal['signal60']})

    df = pd.DataFrame({'price1min':p1['close'],'price5min':p5['close'],'price15min':p15['close'],'price60min':p60['close'],'macd1':macd['macd1'],'signal1':signal['signal1'],'diff1':diff['diff1'],'macd5':macd['macd5'],'signal5':signal['signal5'],'diff5':diff['diff5'],'macd15':macd['macd15'],'signal15':signal['signal15'],'diff15':diff['diff15'],'macd60':macd['macd60'],'signal60':signal['signal60'],'diff60':diff['diff60'],'p1_change':p1_change['close']})

    X = df.drop('p1_change',axis=1).copy()
    y = df['p1_change'].copy()
    X_train = X.copy()
    X_test = X.copy()
    y_train = y.copy()
    y_test = y.copy()
    for i in range(round(len(X)/2)):
        X_train.drop(index=i,inplace=True)
        y_train.drop(index=i,inplace=True)
    for i in range(round(len(X)/2),len(X)):
        X_test.drop(index=i,inplace=True)
        y_test.drop(index=i,inplace=True)
    print(X_train)
    clf_xgb = xgb.XGBClassifier(objective='binary:logistic',seed=42)
    clf_xgb.fit(X_train,y_train,verbose=True)
    print("Done fitting!")
    print(clf_xgb.predict(X_test))
    pd.set_option("display.max_rows", 100, "display.max_columns", 100)
    #comparison = pd.DataFrame({'predictions':preds,'actual':y_test})
    #print(preds)
    '''
    print(comparison)
    comparison = (preds / y_test)*100
    print(comparison.mean())
    '''
machine_learn()
