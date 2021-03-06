import pandas as pd

def rsi(prices):
    df = pd.DataFrame(prices)['close']
    delta = df.diff()
    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = up.ewm(span=14).mean()
    roll_down1 = down.abs().ewm(span=14).mean()
    rsi = roll_up1 / roll_down1
    rsi = 100.0 - (100.0 / (1.0 + rsi))
    return rsi

def ema(prices,length):
    df = pd.DataFrame(prices)['close']
    ema = df.ewm(span=length).mean()
    return ema

def macd(prices):
    df = pd.DataFrame(prices)['close']
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1-exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd,signal
def roc(data,interval):
    df = pd.DataFrame(data)
    return df.pct_change(periods=interval)
