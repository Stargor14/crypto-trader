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
    stopLoss = -(float(input("stop: ")))
    takeProfit = (float(input("take: ")))
    if inTrade == False: #open conditions go here
        if rsi>=70:
            primeds = True
        if primeds == True and signal>macd:
            entry = prices[0]['close']
            broker.short(entry,prices,rsi)
            inTrade = True
            inShort = True
            primeds = False
            primedl = False
        if rsi<=30:
            primedl = True
        if primedl == True and signal<macd:
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
            if pNl>=takeProfit:
                broker.close(exit,takeProfit,prices,rsi,'s')
                inTrade = False
                inShort = False
            if pNl<=stopLoss:
                broker.close(exit,stopLoss,prices,rsi,'s')
                inTrade = False
                inShort = False
        if inLong == True:
            pNl = (exit/entry-1)*100
            if pNl>=takeProfit:
                broker.close(exit,pNl,prices,rsi,'l')
                inTrade = False
                inLong = False
            if pNl<=stopLoss:
                broker.close(exit,pNl,prices,rsi,'l')
                inTrade = False
                inLong = False
