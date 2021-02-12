import broker
import json

global inTrade
global inShort
global inLong
global stoploss
global takeProfit

inTrade = False
inShort = False
inLong = False
stopLoss = float(input("Stop Loss%: "))
takeProfit = float(input("takeProfit%: "))

def run(prices,rsi,dev):
    global inTrade
    global inShort
    global inLong
    global stoploss
    global takeProfit

    cdiff = prices[1][2]-prices[1][1] #price diff whole, check if pos or neg
    ccdiff = prices[0][2]-prices[0][1] #current difference

    if inTrade == False: #open conditions go here
        if rsi>=80 and cdiff<0 and ccdiff<cdiff: #accleerating downward
            entry = prices[0][2]
            broker.short(entry)
            inTrade = True
            inShort = True
        if rsi<=30 and cdiff>0 and ccdiff>cdiff: #accelerating upward
            entry = prices[0][2]
            broker.long(entry)
            inTrade = True
            inLong = True
    if inTrade == True: #close conditions go here
        exit = prices[0][2]
        if inShort == True:
            pNl = -1*((exit/entry[1][1]-1)*100) #reversed for short
            if pNl>=takeProfit:
                broker.close(exit)
            if pNl<=stopLoss:
                broker.close(exit)
                inTrade = False
        if inLong == True:
            pNl = (exit/entry[1][1]-1)*100 #full %: 1%, -2% 5% is 1, -2, 5
            if pNl>=takeProfit:
                broker.close(exit)
                inTrade = False
            if pNl<=stopLoss:
                broker.close(exit)
                inTrade = False
