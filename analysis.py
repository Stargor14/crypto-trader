import broker
import json
global inTrade
global inShort
global inLong
global entry
global exit
global primeds
global primedl

inTrade = False
inShort = False
inLong = False
entry = 1
exit = 1
primeds = False
primedl = False

def run(prices,rsi,macd,signal):
    global inTrade
    global inShort
    global inLong
    global entry
    global exit
    global primeds
    global primedl
    stopLoss = -1

    diff2 = prices[2]['close']-prices[2]['open']
    diff1 = prices[1]['close']-prices[1]['open'] #price diff whole, check if pos or neg
    diff = prices[0]['close']-prices[0]['open'] #current difference

    if inTrade == False: #open conditions go here
        if rsi>=80:
            primeds = True
        if primeds == True and signal<macd:
            entry = prices[0]['close']
            broker.short(entry,prices,rsi)
            inTrade = True
            inShort = True
            primeds = False
            primedl = False
        if rsi<=30:
            primedl = True
        if primedl == True and signal>macd:
            entry = prices[0]['close']
            broker.long(entry,prices,rsi)
            inTrade = True
            inLong = True
            primedl = False
            primeds = False
    if inTrade == True: #close conditions go here
        exit = prices[0]['close']
        if inShort == True:
            pNl = -1*((exit/entry-1)*100) #reversed for short
            pNl1 = -1*((prices[1]['close']/entry-1)*100)
            if signal>macd:
                broker.close(exit,takeProfit,prices,rsi,'s')
                inTrade = False
                inShort = False
            if pNl<=stopLoss:
                broker.close(exit,stopLoss,prices,rsi,'s')
                inTrade = False
                inShort = False
        if inLong == True:
            pNl = (exit/entry-1)*100
            pNl1 = (prices[1]['close']/entry-1)*100
            if signal<macd:
                broker.close(exit,pNl,prices,rsi,'l')
                inTrade = False
                inLong = False
            if pNl<=stopLoss:
                broker.close(exit,pNl,prices,rsi,'l')
                inTrade = False
                inLong = False
