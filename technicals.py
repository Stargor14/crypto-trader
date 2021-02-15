import req
import analysis
import math
import pandas_datareader as pdr
import pandas
rsilength = 14
devlength = 100
global macda
macda = []


def rsi():
    global rsilength
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
    return RSI1[len(prices)-1]

def macd():
    prices=list(reversed(req.prices))
    df = pandas.DataFrame(prices)['close']
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd[len(prices)-1],signal[len(prices)-1]

def run():
    while True:
        prices = req.prices
        analysis.run(prices,rsi(),macd()[0],macd()[1])
        req.run()
req.run()
run()
