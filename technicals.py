import req
import trader
import analysis
import math

rsilength = 15
tf = 1

def rsi():
    prices = req.prices
    g = []
    l = []
    gs = 0
    ls = 0
    for i in range(rsilength):
        if prices[i][2]-prices[i][1]>0:
            g.append(prices[i][2]-prices[i][1])
        if prices[i][2]-prices[i][1]<=0:
            l.append(prices[i][2]-prices[i][1])
    for i in g:
        gs+=i
    for i in l:
        ls+=i
    ag = gs/15
    al = abs(ls/15)
    if ag == 0:
        ag = 1
    if al == 0:
        al = 1
    rs = ag/al
    rsi = round((100 - (100/(1+rs))),2)
    print(f"rsi {rsi}")
    return rsi

def dev():
    prices = req.prices
    sum=0
    for price in prices:
        sum+=price[2]
    diffsum=0
    for price in prices:
        diffsum+=(price[2]-sum/len(prices))**2
    dev = math.sqrt(diffsum/len(prices))
    #print(f"dev {dev}")
    return dev

def run():
    while True:
        prices = req.prices
        analysis.run(prices,rsi(),dev())
        req.run(tf)

req.run(tf)

if len(req.prices)==req.hlength:
    run()
