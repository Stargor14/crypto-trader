import broker
import json
global inShort
global inLong
global stopLosss
global takeProfits
global stopLossl
global takeProfitl
global entryl
global exitl
global entrys
global exits
global primeds
global primedl

inShort = False
inLong = False
stopLosss = -1*(float(input("Stop Loss Short%: ")))
takeProfits = float(input("Take Profit Short%: "))
stopLossl = -1*(float(input("Stop Loss Long%: ")))
takeProfitl = float(input("Take Profit Long %: "))
entryl = 1
exitl = 1
entrys = 1
exits = 1
primeds = False
primedl = False

def run(prices,rsi,macd,signal,row):
    global inShort
    global inLong
    global stopLosss
    global takeProfits
    global stopLossl
    global takeProfitl
    global entryl
    global exitl
    global entrys
    global exits
    global primeds
    global primedl
    rsimax = 70
    rsimin =30

    #enter conditions
    if inShort == False:
        if rsi>=rsimax:
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
