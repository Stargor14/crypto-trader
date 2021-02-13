import req
import analysis
import math

rsilength = 14
devlength = 100

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

def run():
    global row
    while True:
        prices = req.prices
        analysis.run(prices,rsi())
        req.run()
req.run()
run()
