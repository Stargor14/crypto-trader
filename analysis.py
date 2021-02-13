import broker
import json

global inTrade
global inShort
global inLong
global stoploss
global takeProfit
global entry
global exit
global primed

inTrade = False
inShort = False
inLong = False
stopLoss = float(input("Stop Loss%: "))
takeProfit = float(input("takeProfit%: "))
entry = 1
exit = 1
primed = False
def run(prices,rsi,dev,row):
    global inTrade
    global inShort
    global inLong
    global stoploss
    global takeProfit
    global entry
    global exit
    global primed

    diff2 = prices[row+2]['close']-prices[row+2]['open']
    diff1 = prices[row+1]['close']-prices[row+1]['open'] #price diff whole, check if pos or neg
    diff = prices[row]['close']-prices[row]['open'] #current difference

    if inTrade == False: #open conditions go here
        if rsi>=80: #accleerating downward
            primed = True
        if primed == True and diff<-50 and diff1<-50:
            entry = prices[row]['close']
            broker.short(entry)
            inTrade = True
            inShort = True
            primed = False
        '''
        if rsi<=26 and diff2>0 and diff1>0 and diff>0: #accelerating upward
            entry = prices[row]['close']
            broker.long(entry)
            inTrade = True
            inLong = True
        '''
    if inTrade == True: #close conditions go here
        exit = prices[row]['low']
        if inShort == True:
            pNl = -1*((exit/entry-1)*100) #reversed for short
            if pNl>=takeProfit:
                broker.close(exit,pNl)
                inTrade = False
                inShort = False
            if pNl<=stopLoss:
                broker.close(exit,pNl)
                inTrade = False
                inShort = False
        if inLong == True:
            pNl = (exit/entry-1)*100 #full %: 1%, -2% 5% is 1, -2, 5
            if pNl>=takeProfit:
                broker.close(exit,pNl)
                inTrade = False
                inLong = False
            if pNl<=stopLoss:
                broker.close(exit,pNl)
                inTrade = False
                inLong = False
