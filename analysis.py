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
        if rsi>=70 and row>broker.cooldown:
            primeds = True
            primedl = False
            '''
        if primedl == True and signal<macd and rsi>30 and row>broker.cooldown:
            entry = prices[row]['close']
            broker.long(entry,row)
            inTrade = True
            inLong = True
            primedl = False
            '''
        if rsi<=30 and row>broker.cooldown:
            primedl = True
            primeds = False

        if primedl == True and signal>macd and rsi<70 and row>broker.cooldown:
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
            exitl = prices[row]['low']
            exith = prices[row]['high']
            pNll = (exitl/entry-1)*100
            pNlh = (exith/entry-1)*100
            if pNlh>=takeProfit or signal>macd and pNlh>=takeProfit/4 or rsi>70  and pNlh>=takeProfit/4:
                broker.close(exith,pNlh,row,'l')
                inTrade = False
                inLong = False
            if pNll<=stopLoss:
                broker.close(exitl,stopLoss,row,'l')
                inTrade = False
                inLong = False
        if inShort == True:
            exitl = prices[row]['low']
            exith = prices[row]['high']
            pNll = -(exitl/entry-1)*100
            pNlh = -(exith/entry-1)*100
            if pNll>=takeProfit or signal<macd and pNll>=takeProfit/4 or rsi<30  and pNll>=takeProfit/4:
                broker.close(exitl,pNll,row,'s')
                inTrade = False
                inShort = False
            if pNlh<=stopLoss:
                broker.close(exith,stopLoss,row,'s')
                inTrade = False
                inShort = False
