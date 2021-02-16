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
stopLoss = -1*(float(input("Stop Loss %: ")))
takeProfit = float(input("Take Profit %: "))
entry = 1
exit = 1
primeds = False
primedl = False

def run(prices,rsi,macd,signal,row):
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
    diff2 = prices[row+2]['close']-prices[row+2]['open']
    diff1 = prices[row+1]['close']-prices[row+1]['open'] #price diff whole, check if pos or neg
    diff = prices[row]['close']-prices[row]['open'] #current difference

    if inTrade == False: #open conditions go here
        if rsi>=70:
            primeds = True
            primedl = False
        if primedl == True and signal<macd:
            entry = prices[row]['close']
            broker.long(entry,row)
            inTrade = True
            inLong = True
            primedl = False
        if rsi<=30:
            primedl = True
            primeds = False
        if primeds == True and signal>macd:
            entry = prices[row]['close']
            broker.short(entry,row)
            inTrade = True
            inShort = True
            primeds = False
        #if rsi>45 and rsi<55:
            #primedl = False
            #primeds = False
    if inTrade == True: #close conditions go here
        if inLong == True:
            exit = prices[row]['close']
            pNl = (exit/entry-1)*100 #reversed for short
            if pNl>=takeProfit:
                broker.close(exit,pNl,row)
                inTrade = False
                inLong = False
            if pNl<=stopLoss:
                broker.close(exit,stopLoss,row)
                inTrade = False
                inLong = False
        if inShort == True:
            exit = prices[row]['close']
            pNl = -(exit/entry-1)*100 #full %: 1%, -2% 5% is 1, -2, 5
            if pNl>=takeProfit:
                broker.close(exit,pNl,row)
                inTrade = False
                inShort = False
            if pNl<=stopLoss:
                broker.close(exit,stopLoss,row)
                inTrade = False
                inShort = False
