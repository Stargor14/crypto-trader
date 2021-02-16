import req
import math
import pandas
import json
import time

def rsi(rsilength):
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

def macd():
    prices=req.prices
    df = pandas.DataFrame(prices)['close']
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd,signal

def test(prices,rsia,macda,signala,takeProfit,stopLoss):
    primeds = False
    primedl = False
    inTrade = False
    inLong = False
    inShort = False
    balance = 100
    rsimax = 70
    rsimin =30
    trades=0
    for i in range(len(prices)):
        if inTrade == False:
            entry = prices[i]['close']
            if rsia[i]>=rsimax:
                primeds = True
                primedl = False
            if primedl == True and signala[i]<macda[i] and rsia[i]>rsimin:
            #if primedl == True and rsia[i]>rsimin:
                inTrade = True
                inLong = True
                primedl = False
            if rsia[i]<=rsimin:
                primedl = True
                primeds = False
            if primeds == True and signala[i]>macda[i] and rsia[i]<rsimax:
            #if primeds == True and rsia[i]<rsimax:
                inTrade = True
                inShort = True
                primeds = False
            #if ((rsimax+rsimin)/2)-((rsimax+rsimin)/20)<rsi<((rsimax+rsimin)/2)+((rsimax+rsimin)/20):
                #primedl = False
                #primeds = False
        if inTrade == True:
            if inLong == True:
                exitl = prices[i]['low']
                exith = prices[i]['high']
                pNll = (exitl/entry-1)*100
                pNlh = (exith/entry-1)*100
                if pNlh>=takeProfit or signala[i]>macda[i] and pNlh>=takeProfit/2 or rsia[i]>rsimax  and pNlh>=takeProfit/2:
                    balance=balance*(((pNlh-.08)/100)+1)
                    trades+=1
                    inTrade = False
                    inLong = False
                if pNll<=stopLoss:
                    balance=balance*(((stopLoss-.08)/100)+1)
                    trades+=1
                    inTrade = False
                    inLong = False
            if inShort == True:
                exitl = prices[i]['low']
                exith = prices[i]['high']
                exitc = prices[i]['close']
                pNll = -(exitl/entry-1)*100
                pNlh = -(exith/entry-1)*100
                if pNll>=takeProfit or signala[i]<macda[i] and pNll>=takeProfit/2 or rsia[i]<rsimin  and pNll>=takeProfit/2:
                    balance=balance*(((pNll-.08)/100)+1)
                    trades+=1
                    inTrade = False
                    inShort = False
                if pNlh<=stopLoss :
                    balance=balance*(((stopLoss-.08)/100)+1)
                    trades+=1
                    inTrade = False
                    inShort = False
    return balance,trades

def sorter(i):
    return i['BALANCE']

def run():
    macda = macd()[0]
    signala = macd()[1]
    prices = req.prices
    num = 0
    runs = 12*20*20
    dataset=[{"RSI LENGTH":0,"TAKE PROFIT":0,"STOP LOSS":0,"BALANCE":0,"TRADES":0}]
    for rsilength in range(8,20):
        for takeProfit in range(10,30):
            for stopLoss in range(-30,-10):
                if num%10==0 and num>0:
                    print(f"{num}/{runs} Expected time remaining: {(runs-num)*runtime} seconds")
                tic = time.perf_counter()
                balance = test(prices,rsi(rsilength),macda,signala,takeProfit/10,stopLoss/10)
                if balance[0]>=dataset[0]['BALANCE']:
                    dataset.append({"RSI LENGTH":rsilength,"TAKE PROFIT":takeProfit,"STOP LOSS":stopLoss,"BALANCE":balance[0],"TRADES":balance[1]})
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
        print(f"rank: {j} RSI length: {i['RSI LENGTH']} Take Profit: {i['TAKE PROFIT']/10} Stop Loss: {i['STOP LOSS']/10} Balance: {round(i['BALANCE'],4)} Trades: {i['TRADES']}")
        j-=1
req.run()
run()
