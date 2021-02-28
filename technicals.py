import req
import analysis
import math
import pandas
import matplotlib.pyplot as plt
import broker

global row
row = 0

def rsi():
    prices = req.prices
    df = pandas.DataFrame(prices)['close']
    delta = df.diff()
    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = up.ewm(span=14).mean()
    roll_down1 = down.abs().ewm(span=14).mean()
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    print(RSI1)
    return RSI1

def ema(length):
    prices = req.prices
    df = pandas.DataFrame(prices)['close']
    ema = df.ewm(span=length).mean()
    return ema

def macd():
    prices=req.prices
    df = pandas.DataFrame(prices)['close']
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd,signal

def run():
    global row

    if input("Graph?") != "":
        graph = True
    else:
        graph = False
    prices = req.prices
    macda = macd()[0]
    signala = macd()[1]
    rsia = rsi()
    df = pandas.DataFrame(prices)['close']
    while row<=len(prices)-1:
        analysis.run(prices,rsia[row],macda[row],signala[row],row)
        row+=1
    if row==len(prices) and graph == True:
        trades = broker.trades
        macda.plot(label='BTC MACD', color='g')
        ax = signala.plot(label='Signal Line', color='r')
        df.plot(ax=ax, secondary_y=True, label='BTC')
        ax.set_ylabel('MACD')
        ax.right_ax.set_ylabel('Price $')
        ax.set_xlabel('CANDLE')
        lines = ax.get_lines() + ax.right_ax.get_lines()
        ax.legend(lines, [l.get_label() for l in lines], loc='upper left')
        x_list = [x for [x, y,z] in trades]
        y_list = [y for [x, y,z] in trades]
        z_list = [z for [x, y,z] in trades]
        for i in range(len(x_list)):
            if z_list[i]=='s':
                plt.scatter(x_list[i], y_list[i],color='r')
            if z_list[i]=='l':
                plt.scatter(x_list[i], y_list[i],color='g')
            if z_list[i]=='c':
                plt.scatter(x_list[i], y_list[i],color='b')
        plt.show()
req.run()
run()
