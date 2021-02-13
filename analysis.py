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

def run(prices,rsi):
    global inTrade
    global inShort
    global inLong
    global entry
    global exit
    global primeds
    global primedl
    stopLoss = -.2
    takeProfit = .6

    diff2 = prices[2]['close']-prices[2]['open']
    diff1 = prices[1]['close']-prices[1]['open'] #price diff whole, check if pos or neg
    diff = prices[0]['close']-prices[0]['open'] #current difference

    if inTrade == False: #open conditions go here
        if rsi>=80:
            primeds = True
        if primeds == True and diff<-50 and diff1<-50:
            entry = prices[0]['close']
            broker.short(entry,prices,rsi)
            inTrade = True
            inShort = True
            primeds = False
        if rsi<=30:
            primedl = True
        if primedl == True and diff1>50 and diff>50:
            entry = prices[0]['close']
            broker.long(entry,prices,rsi)
            inTrade = True
            inLong = True
            primedl = False
    if inTrade == True: #close conditions go here
        exit = prices[0]['close']
        if inShort == True:
            pNl = -1*((exit/entry-1)*100) #reversed for short
            if pNl>=takeProfit:
                broker.close(exit,pNl,prices,rsi)
                inTrade = False
                inShort = False
            if pNl<=stopLoss:
                broker.close(exit,pNl,prices,rsi)
                inTrade = False
                inShort = False
        if inLong == True:
            pNl = (exit/entry-1)*100 #full %: 1%, -2% 5% is 1, -2, 5
            if pNl>=takeProfit:
                broker.close(exit,pNl,prices,rsi)
                inTrade = False
                inLong = False
            if pNl<=stopLoss:
                broker.close(exit,pNl,prices,rsi)
                inTrade = False
                inLong = False
