import broker
import json
import req

global inShort
global inLong
global entry
global exit
global init

inShort = False
inLong = False
init = True

def run(prices,rsi,macd,signal,row):
    global inShort
    global inLong
    global entry
    global exit
    global init
    stopLoss = 1
    if init==True:
        entry = prices[row]['close']
        exit = prices[row]['close']
        exitl = prices[row]['low']
        exith = prices[row]['high']
        init = False
    #enter conditions
    if inShort == False:
        if signal>macd or (entry/exit-1)*100 <= -stopLoss:
            exit = prices[row]['close']
            exitl = prices[row]['low']
            exith = prices[row]['high']
            pNl = (entry/exit-1)*100
            pNll = (entry/exitl-1)*100
            pNlh = (entry/exith-1)*100
            if pNl>0:
                broker.close(exit,pNl,row,'l')
                inLong = False
                entry = prices[row]['close']
                broker.short(entry,row)
                inShort = True
            if pNll<=-stopLoss or pNlh <=-stopLoss:
                broker.close(exit,-stopLoss,row,'l')
                inLong = False
                entry = prices[row]['close']
                broker.short(entry*(100-stopLoss)/100,row)
                inShort = True
    if inLong == False:
        if signal<macd or (exit/entry-1)*100 <= -stopLoss:
            exit = prices[row]['close']
            exitl = prices[row]['low']
            exith = prices[row]['high']
            pNl = (entry/exit-1)*100
            pNll = (entry/exitl-1)*100
            pNlh = (entry/exith-1)*100
            if pNll<-stopLoss or pNlh <-stopLoss:
                broker.close(exit,-stopLoss,row,'s')
                inShort = False
                entry = prices[row]['close']
                broker.long(entry*(100-stopLoss)/100,row)
                inLong = True
            if pNl>0:
                broker.close(exit,pNl,row,'s')
                inShort = False
                entry = prices[row]['close']
                broker.long(entry,row)
                inLong = True
