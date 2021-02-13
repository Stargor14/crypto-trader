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

def run(prices,rsi,dev,row):
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
        if rsi>=80:
            primeds = True
        if primeds == True and diff<-50 and diff1<-50:
            entry = prices[row]['close']
            broker.short(entry)
            inTrade = True
            inShort = True
            primeds = False
        if rsi<=30:
            primedl = True
        if primedl == True and diff2>50 and diff1>50 and diff>50:
            entry = prices[row]['close']
            broker.long(entry)
            inTrade = True
            inLong = True
            primedl = False
    if inTrade == True: #close conditions go here
        if inShort == True:
            exit = prices[row]['low']
            pNl = -1*((exit/entry-1)*100) #reversed for short
            if pNl>=takeProfit:
                broker.close(exit,takeProfit)
                inTrade = False
                inShort = False
            if pNl<=stopLoss:
                broker.close(exit,stopLoss)
                inTrade = False
                inShort = False
        if inLong == True:
            exit = prices[row]['high']
            pNl = (exit/entry-1)*100 #full %: 1%, -2% 5% is 1, -2, 5
            if pNl>=takeProfit:
                broker.close(exit,takeProfit)
                inTrade = False
                inLong = False
            if pNl<=stopLoss:
                broker.close(exit,stopLoss)
                inTrade = False
                inLong = False
