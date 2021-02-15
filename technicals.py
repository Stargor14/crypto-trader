import req
import backtest
import math
import pandas
import broker


rsilength = 14

global row
row = 0
def rsi():
    global row
    global rsilength
    prices = req.prices
    df = pandas.DataFrame(prices)['close']
    delta = df.diff()
    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = up.ewm(span=rsilength).mean()
    roll_down1 = down.abs().ewm(span=rsilength).mean()
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    print(RSI1)
    return RSI1

def macd():
    prices=req.prices
    df = pandas.DataFrame(prices)['close']
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd,signal

def run():
    macda = macd()[0]
    signala = macd()[1]
    for rsimax in range(60,80):
        for rsimin in range(25,40):
            for rsilength in range(5,20):
                for takeProfit in range(0,2,.01):
                    for stopLoss in range(0,2,.01):

    prices = req.prices
    rsia = rsi()
    df = pandas.DataFrame(prices)['close']
    while row<=len(prices)-100:
        analysis.run(prices,rsia[row],macda[row],signala[row],row)
        row+=1
req.run()
run()
