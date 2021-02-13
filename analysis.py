import broker
import json
global inTrade
global inShort
global inLong
global Sstoploss
global StakeProfit
global Lstoploss
global LtakeProfit
global entry
global exit
global primeds
global primedl

inTrade = False
inShort = False
inLong = False
stopLoss = -1*(float(input("Stop Loss Short%: ")))
takeProfit = float(input("Take Profit Short%: "))
LstopLoss = -1*(float(input("Stop Loss Long%: ")))
LtakeProfit = float(input("Take Profit Long%: "))
entry = 1
exit = 1
primeds = False
primedl = False

def run(prices,rsi):
    global inTrade
    global inShort
    global inLong
    global Sstoploss
    global StakeProfit
    global Lstoploss
    global LtakeProfit
    global entry
    global exit
    global primeds
    global primedl
    diff2 = prices[2]['close']-prices[2]['open'] # difference 2 candles ago
    diff1 = prices[1]['close']-prices[1]['open'] #difference 1 candle ago
    diff = prices[0]['close']-prices[0]['open'] #current difference

    if inTrade == False: #open conditions go here
        if rsi>=80:
            primeds = True
        if primeds == True and diff1<-20 and diff<-20:
            entry = prices[0]['close']
            broker.short(entry,prices,rsi)
            inTrade = True
            inShort = True
            primeds = False
        if rsi<=30:
            primedl = True
        if primedl == True and diff1>20 and diff>20:
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
