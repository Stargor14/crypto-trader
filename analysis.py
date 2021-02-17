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
    rsimax = 70
    rsimin =30

    #enter conditions
    if inShort == False:
        if rsi[row]>=rsimax:
            primeds = True
        if primeds == True and signal>macd and rsi<=rsimax:
            entrys = prices[row]['close']
            inShort = True
            primeds = False
    if inLong == False:
        if rsi<=rsimin:
            primedl = True
        if primedl == True and signal<macd and rsi>=rsimin:
            entryl = prices[row]['close']
            inLong = True
            primedl = False
    if 45<rsi<55:
        primedl = False
        primeds = False
        #close conditions
    exitl = prices[row]['low']
    exith = prices[row]['high']
    exitc = prices[row]['close']
    if inLong == True:
        pNll = (exitl/entryl-1)*100
        pNlh = (exith/entryl-1)*100
        if pNlh>=takeProfitl or signal>macd and pNlh>=takeProfitl/4 or rsi>rsimax  and pNlh>=takeProfitl/4:
            broker.close(exith,pNlh,row,'l')
            inLong = False
        if pNll<=stopLossl:
            broker.close(exitl,stopLossl,row,'l')
            inLong = False
    if inShort == True:
        pNll = -(exitl/entrys-1)*100
        pNlh = -(exith/entrys-1)*100
        if pNll>=takeProfits or signal<macd and pNll>=takeProfits/4 or rsi<rsimin  and pNll>=takeProfits/4:
            broker.close(exitl,pNll,row,'s')
            inShort = False
        if pNlh<=stopLosss :
            broker.close(exith,stopLosss,row,'s')
            inShort = False
