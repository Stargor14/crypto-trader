import req
import math
import pandas
import json
import time

def rsicur(rsilength):
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

def macdcur():
    prices=req.prices
    df = pandas.DataFrame(prices)['close']
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd,signal
def test(prices,rsia,macda,signala,takeProfits,stopLosss,takeProfitl,stopLossl):
    primeds = False
    primedl = False
    inLong = False
    inShort = False
    balance = 100
    rsimax = 60
    rsimin =40
    trades=0
    shortg =0
    longg =0
    shortb =0
    longb = 0
    for i in range(len(prices)):
        #enter conditions
        if inShort == False:
            if rsia[i]>=rsimax:
                primeds = True
            if primeds == True and signala[i]>macda[i] and rsia[i]<=rsimax:
                entrys = prices[i]['close']
                inShort = True
                primeds = False
        if inLong == False:
            if rsia[i]<=rsimin:
                primedl = True
            if primedl == True and signala[i]<macda[i] and rsia[i]>=rsimin:
                entryl = prices[i]['close']
                inLong = True
                primedl = False
        #close conditions
        exitl = prices[i]['low']
        exith = prices[i]['high']
        exitc = prices[i]['close']

        if inLong == True:
            pNll = (exitl/entryl-1)*100
            pNlh = (exith/entryl-1)*100
            if pNlh>=takeProfitl or signala[i]>macda[i] and pNlh>=takeProfitl/4 or rsia[i]>rsimax  and pNlh>=takeProfitl/4:
                balance=balance*(((pNlh-.08)/100)+1)
                trades+=1
                inLong = False
                longg+=1
            if pNll<=stopLossl:
                balance=balance*(((stopLossl-.08)/100)+1)
                trades+=1
                inLong = False
                longb+=1
        if inShort == True:
            pNll = -(exitl/entrys-1)*100
            pNlh = -(exith/entrys-1)*100
            if pNll>=takeProfits or signala[i]<macda[i] and pNll>=takeProfits/4 or rsia[i]<rsimin  and pNll>=takeProfits/4:
                balance=balance*(((pNll-.08)/100)+1)
                trades+=1
                inShort = False
                shortg+=1
            if pNlh<=stopLosss :
                balance=balance*(((stopLosss-.08)/100)+1)
                trades+=1
                inShort = False
                shortb+=1

    return balance,trades,shortg,shortb,longg,longb
def sorter(i):
    return i['BALANCE']
def run():
    macda = macdcur()[0]
    signala = macdcur()[1]
    rsia = rsicur(14)
    prices = req.prices
    num = 0
    runs = 12*2*12*2
    rsilength = 14
    dataset=[{"TAKE PROFITL":0,"STOP LOSSL":0,"TAKE PROFITS":0,"STOP LOSSS":0,"BALANCE":0,"TRADES":0,"SHORTG":0,"SHORTB":0,"LONGG":0,"LONGB":0}]
    takeProfitl = 0
    stopLossl = -0
    takeProfith = 0
    stopLossh = -0
    for takeProfitl in range(40,42):
        for stopLossl in range(-10,-8):
            for takeProfits in range(38,48):
                for stopLosss in range(-17,-10):
                    if num%10==0 and num>0:
                        print(f"{num}/{runs} Expected time remaining: {round((runs-num)*runtime,1)} seconds")
                    tic = time.perf_counter()
                    balance = test(prices,rsia,macda,signala,takeProfits/10,stopLosss/10,takeProfitl/10,stopLossl/10)
                    if balance[0]>=dataset[0]['BALANCE']:
                        dataset.append({"TAKE PROFITL":takeProfitl,"STOP LOSSL":stopLossl,"TAKE PROFITS":takeProfits,"STOP LOSSS":stopLosss,"BALANCE":balance[0],"TRADES":balance[1], "SHORTG":balance[2], "SHORTB":balance[3], "LONGG":balance[4], "LONGB":balance[5]})
                        dataset.sort(key=sorter)
                        if len(dataset)>50:
                            dataset.pop(0)
                    toc = time.perf_counter()
                    runtime = (toc-tic)
                    num+=1
    with open("Z:\github\data.json", "w") as write_file:
        json.dump(dataset, write_file)
    j=50
    for i in dataset:
        print(f"rank: {j} TPL: {i['TAKE PROFITL']/10} SLL: {i['STOP LOSSL']/10} TPS: {i['TAKE PROFITS']/10} SLS: {i['STOP LOSSS']/10} Balance: {round(i['BALANCE'],2)} Trades: {i['TRADES']} Short G/B: {i['SHORTG']}/{i['SHORTB']} LONG G/B: {i['LONGG']}/{i['LONGB']}")
        j-=1
req.run()
run()
