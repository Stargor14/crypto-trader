import req
import math
import pandas
import broker
import json

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

def test(prices,rsi,macda,signala,takeProfit,stopLoss):
    primeds = False
    primedl = False
    inTrade = False
    inLong = False
    inShort = False
    balance = 1
    rsimax=70
    rsimin=30
    for candle in prices:
        if inTrade == False:
            entry = candle['close']
            if rsi>=rsimax:
                primeds = True
                primedl = False
            if primedl == True and signala<macda:
                inTrade = True
                inLong = True
                primedl = False
            if rsi<=rsimin:
                primedl = True
                primeds = False
            if primeds == True and signala>macda:
                inTrade = True
                inShort = True
                primeds = False
            if ((rsimax+rsimin)/2)-((rsimax+rsimin)/20)<rsi<((rsimax+rsimin)/2)+((rsimax+rsimin)/20):
                primedl = False
                primeds = False
        if inTrade == True:
            if inLong == True:
                exit = candle['high']
                pNl = (exit/entry-1)*100
                if pNl>=takeProfit:
                    balance=balance*((takeProfit/100)+1)
                    inTrade = False
                    inLong = False
                if pNl<=stopLoss:
                    balance=balance*((stopLoss/100)+1)
                    inTrade = False
                    inLong = False
            if inShort == True:
                exit = candle['low']
                pNl = -(exit/entry-1)*100
                if pNl>=takeProfit:
                    balance=balance*((takeProfit/100)+1)
                    inTrade = False
                    inShort = False
                if pNl<=stopLoss:
                    balance=balance*((stopLoss/100)+1)
                    inTrade = False
                    inShort = False
    return balance

def sorter(i):
    return i['BALANCE']

def run():
    macda = macd()[0]
    signala = macd()[1]
    prices = req.prices
    dataset=[{"RSI LENGTH":0,"TAKE PROFIT":0,"STOP LOSS":0,"BALANCE":0}]
    num = 0
    for rsilength in range(5,20):
        for takeProfit in range(0,20):
            for stopLoss in range(-20,0):
                if num%1000==0:
                    print(num)
                balance = test(prices,rsi(rsilength)[num],macda[num],signala[num],takeProfit/10,stopLoss/10)
                if balance>=dataset[0]['BALANCE']:
                    dataset.append({"RSI LENGTH":rsilength,"TAKE PROFIT":takeProfit,"STOP LOSS":stopLoss,"BALANCE":balance})
                    dataset.sort(key=sorter)
                    if len(dataset)>50:
                        dataset.pop(0)
                num+=1
    print(dataset)

    with open("Z:\github\data.json", "w") as write_file:
        json.dump(dataset, write_file)

#PRINT THE DATASET <------------------------------------------------------------------------------------------------------------------|
req.run()
run()
