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

    if init==True:
        entry = prices[row]['close']
        exit = prices[row]['close']
        init = False
    #enter conditions
    if inShort == False:
        if signal>macd or (exit/entry-1)*100 < -1:
            exit = prices[row]['close']
            pNl = (entry/exit-1)*100
            broker.close(exit,pNl,row,'l')
            inLong = False
            entry = prices[row]['close']
            broker.short(entry,row)
            inShort = True
    if inLong == False:
        if signal<macd or (entry/exit-1)*100 < -1:
            exit = prices[row]['close']
            pNl = (entry/exit-1)*100
            broker.close(exit,pNl,row,'s')
            inShort = False
            entry = prices[row]['close']
            broker.long(entry,row)
            inLong = True
