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
    diff2s = prices[2]['low']-prices[2]['open'] # difference 2 candles ago
    diff1s = prices[1]['low']-prices[1]['open'] #difference 1 candle ago
    diffs = prices[0]['close']-prices[0]['open'] #current difference
    diff2l = prices[2]['high']-prices[2]['open'] # difference 2 candles ago
    diff1l = prices[1]['high']-prices[1]['open'] #difference 1 candle ago
    diffl = prices[0]['close']-prices[0]['open'] #current difference

    if inTrade == False: #open conditions go here
        if rsi>=80:
            primeds = True
            print("Primed for short!")
        if primeds == True and diff1s<-50 and diffs<-50:
            entry = prices[0]['close']
            broker.short(entry,prices,rsi)
            inTrade = True
            inShort = True
            primeds = False
        if rsi<=30:
            primedl = True
            print("Primed for long!")
        if primedl == True and diff1l>50 and diffl>50:
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
