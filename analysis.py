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
global lol

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
lol = 0

def run(prices,rsi,macd,signal):
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
    global lol
    rsimax = 70
    rsimin =30

    #enter conditions
    if inShort == False:
        if rsi>=rsimax:
            primeds = True
        if primeds == True and signal>macd and rsi<=rsimax:
            entrys = prices[0]['close']
            broker.short(entrys,prices,rsi)
            inShort = True
            primeds = False
    if inLong == False:
        if rsi<=rsimin:
            primedl = True
        if primedl == True and signal<macd and rsi>=rsimin:
            entryl = prices[0]['close']
            broker.long(entryl,prices,rsi)
            inLong = True
            primedl = False
    if 45<rsi<55:
        primedl = False
        primeds = False
        #close conditions
    exit = prices[0]['close']
    if inLong == True:
        pNll = (exit/entryl-1)*100
        if pNl>=takeProfitl or signal>macd and pNl>=takeProfitl/4 or rsi>rsimax  and pNl>=takeProfitl/4:
            broker.close(exit,pNl,prices,rsi,'l')
            inLong = False
        if pNll<=stopLossl:
            broker.close(exit,pNl,prices,rsi,'l')
            inLong = False
    if inShort == True:
        pNl = -(exit/entrys-1)*100
        if pNl>=takeProfits or signal<macd and pNl>=takeProfits/4 or rsi<rsimin  and pNl>=takeProfits/4:
            broker.close(exit,pNl,prices,rsi,'s')
            inShort = False
        if pNl<=stopLosss :
            broker.close(exit,pNl,prices,rsi,'s')
            #ex,pnl,prices,rsi,type
            inShort = False
    broker.close(0,0,prices,0,'l')
