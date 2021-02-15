import req
import analysis
import math

rsilength = 14
devlength = 100
global macda
macda = []

def rsi():
    global row
    prices = req.prices
    g = []
    l = []
    gs = 0
    ls = 0
    for i in range(rsilength):
        if prices[i]['close']-prices[i]['open']>0:
            g.append(prices[i]['close']-prices[i]['open'])
        if prices[i]['close']-prices[i]['open']<=0:
            l.append(prices[i]['close']-prices[i]['open'])
    for i in g:
        gs+=i
    for i in l:
        ls+=i
    ag = gs/rsilength
    al = abs(ls/rsilength)
    if ag == 0:
        ag = 1
    if al == 0:
        al = 1
    rs = ag/al
    rsi = round((100 - (100/(1+rs))),2)
    return rsi

def sma(len,target):
    prices = req.prices
    sum=0
    for i in range(len):
        sum+=prices[target]['close']
    sma = sum/len
    return sma

def ema(len,target):
    prices = req.prices
    ema =[]
    n=0
    for i in reversed(range(len)):
        if i == len-1:
            ema.append(sma(len,target+i))
            n+=1
        else:
        # multiplier: (2 / (length + 1))
        # EMA: (close * multiplier) + ((1 - multiplier) * EMA(previous))
            multiplier = 2 / (len + 1)
            ema.append((prices[i+target]['close'] * multiplier) + (ema[n-1]*(1 - multiplier)))
            n+=1
    return ema[len-1]

def macd(target):
    ema26 = ema(26,target)
    ema12 = ema(12,target)
    macd = ema12 - ema26
    return macd

def sigsma(macd):
    sum=0
    for i in range(9):
        sum+=macd[i+8]
    sma = sum/9
    return sma

def signal(macd):
    ema=[]
    n=0
    for i in reversed(range(9)):
        if i == 8:
            ema.append(sigsma(macd))
            n+=1
        else:
        # multiplier: (2 / (length + 1))
        # EMA: (close * multiplier) + ((1 - multiplier) * EMA(previous))
            multiplier = 2 / (9 + 1)
            ema.append((macd[i] * multiplier) + (ema[n-1]*(1 - multiplier)))
            n+=1
    return ema[8]

#macd init
# for i in reverse(range(9)):
#   macd(i)
#getting current macd will be macd(0)

def run():
    while True:
        prices = req.prices
        m=[]
        for i in range(18):
            m.append(macd(i))
        analysis.run(prices,rsi(),macd(0),signal(m))
        print(macd(0),signal(m))
        req.run()

req.run()
run()

'''
def macd():
    macda = []
    prices = req.prices
    for c in range(9):
        ema26 = [] #index 0 is oldest old -> new
        ema12 = [] #index 0 is oldest old -> new
        for i in range(26):
            if i == 0:
                ema26.append(emaprep(26,c)[0])
            else:
                ema26.append((prices[25-i+c]['close']*emaprep(26,c)[1])+(ema26[i-1]*(1-emaprep(26,c)[1])))
        for i in range(12):
            if i == 0:
                ema12.append(emaprep(12,c)[0])
            else:
                ema12.append((prices[11-i+c]['close']*emaprep(12,c)[1])+(ema12[i-1]*(1-emaprep(12,c)[1])))
        macda.append(ema12[8]-ema26[8])
    return({"macd":macda[8],"signal":signal(macda)})
'''
'''
def dev():
    global row
    prices = req.prices
    sum=0
    for i in range(devlength):
        sum+=prices[i]['close']
    diffsum=0
    for i in range(devlength):
        diffsum+=(prices[i]['close']-sum/devlength)**2
    dev = math.sqrt(diffsum/devlength)
    return dev
'''
