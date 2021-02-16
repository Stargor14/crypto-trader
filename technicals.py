import req
import math
import pandas
import json
import time

def rsih(rsilength):
    prices = req.prices
    df = pandas.DataFrame(prices)['high']
    delta = df.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = up.ewm(span=rsilength).mean()
    roll_down1 = down.abs().ewm(span=rsilength).mean()
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    return RSI1
def rsil(rsilength):
    prices = req.prices
    df = pandas.DataFrame(prices)['low']
    delta = df.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = up.ewm(span=rsilength).mean()
    roll_down1 = down.abs().ewm(span=rsilength).mean()
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    return RSI1
def rsia(rsilength):
    prices = req.prices
    df = pandas.DataFrame(prices)['close']
    delta = df.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = up.ewm(span=rsilength).mean()
    roll_down1 = down.abs().ewm(span=rsilength).mean()
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    return RSI1
def macdh():
    prices=req.prices
    df = pandas.DataFrame(prices)['high']
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd,signal
def macdl():
    prices=req.prices
    df = pandas.DataFrame(prices)['low']
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd,signal
def macda():
    prices=req.prices
    df = pandas.DataFrame(prices)['close']
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd,signal
def test(prices,rsia,macda,signala,takeProfits,stopLosss,takeProfitl,stopLossl,):
    primeds = False
    primedl = False
    inLong = False
    inShort = False
    balance = 100
    rsimax = 70
    rsimin =30
    trades=0
    for i in range(len(prices)):
        #enter conditions
        if inShort == False:
            if rsia[i]>=rsimax:
                primeds = True
            if primeds == True and signala[i]>macda[i] and rsia[i]<=rsimax:
                entry = prices[i]['close']
                inShort = True
                primeds = False
        if inLong == False:
            if rsia[i]<=rsimin:
                primedl = True
            if primedl == True and signala[i]<macda[i] and rsia[i]>=rsimin:
                inLong = True
                primedl = False
        if 45<rsia[i]<55:
            primedl = False
            primeds = False
        #close conditions
        exitl = prices[i]['low']
        exith = prices[i]['high']
        exitc = prices[i]['close']
        if inLong == True:
            pNll = (exitl/entry-1)*100
            pNlh = (exith/entry-1)*100
            if pNlh>=takeProfitl or signalh[i]>macdh[i] and pNlh>=takeProfitl/4 or rsih[i]>rsimax  and pNlh>=takeProfitl/4:
                balance=balance*(((pNlh-.08)/100)+1)
                trades+=1
                inLong = False
            if pNll<=stopLossl:
                balance=balance*(((stopLossl-.08)/100)+1)
                trades+=1
                inLong = False
        if inShort == True:
            pNll = -(exitl/entry-1)*100
            pNlh = -(exith/entry-1)*100
            if pNll>=takeProfits or signall[i]<macdl[i] and pNll>=takeProfits/4 or rsil[i]<rsimin  and pNll>=takeProfits/4:
                balance=balance*(((pNll-.08)/100)+1)
                trades+=1
                inShort = False
            if pNlh<=stopLosss :
                balance=balance*(((stopLosss-.08)/100)+1)
                trades+=1
                inShort = False
    return balance,trades
def sorter(i):
    return i['BALANCE']
def run():
    macdl = macdl()[0]
    signall = macdl()[1]
    macdh = macdh()[0]
    signalh = macdh()[1]
    macda = macda()[0]
    signala = macda()[1]
    prices = req.prices
    rsih = rsih(14)
    rsil = rsil(14)
    rsia = rsia(14)
    num = 0
    runs = 25*25
    rsilength = 14
    dataset=[{"TAKE PROFITL":0,"STOP LOSSL":0,"TAKE PROFITS":0,"STOP LOSSS":0,"BALANCE":0,"TRADES":0}]
    takeProfitl = 29
    stopLossl = -23
    for takeProfits in range(5,30):
        for stopLosss in range(-30,-5):
            if num%10==0 and num>0:
                print(f"{num}/{runs} Expected time remaining: {(runs-num)*runtime} seconds")
            tic = time.perf_counter()
            balance = test(prices,rsih,rsil,rsia,macdh,signalh,macdl,signall,macda,signala,takeProfits/10,stopLosss/10,takeProfitl/10,stopLossl/10)
            if balance[0]>=dataset[0]['BALANCE']:
                dataset.append({"TAKE PROFITL":takeProfitl,"STOP LOSSL":stopLossl,"TAKE PROFITS":takeProfits,"STOP LOSSS":stopLosss,"BALANCE":balance[0],"TRADES":balance[1]})
                dataset.sort(key=sorter)
                if len(dataset)>50:
                    dataset.pop(0)
            toc = time.perf_counter()
            runtime = round(toc-tic,1)
            num+=1
    #print("Michael is obese and we need to code thge email thingy rn ASAP Rocky type beat")
    with open("Z:\github\data.json", "w") as write_file:
        json.dump(dataset, write_file)
    j=50
    for i in dataset:
        print(f"rank: {j} TPL: {i['TAKE PROFITL']/10} SLL: {i['STOP LOSSL']/10} TPS: {i['TAKE PROFITS']/10} SLS: {i['STOP LOSSS']/10} Balance: {round(i['BALANCE'],2)} Trades: {i['TRADES']}")
        j-=1
req.run()
run()
