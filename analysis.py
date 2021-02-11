import req
import trader
import math

rsilength = 14
tf = 1

def loop():
    req.run(tf)
    run()

def run():
    gs = 0
    ls = 0
    for i in range(rsilength):
        if ((req.prices[i][2]/req.prices[i][1])-1)>0:
            gs+=(req.prices[i][2]/req.prices[i][1])-1
        if ((req.prices[i][2]/req.prices[i][1])-1)>0:
            ls+=(req.prices[i][2]/req.prices[i][1])-1
    ag = gs/14
    al = abs(ls/14)
    if ag == 0:
        ag = 1
    if al == 0:
        al = 1
    rs = ag/al
    rsi = (100 - (100/(1+rs)))
    print(f"rsi {ag} price {req.prices[0][2]}")
    trader.check(rsi)
    loop()

req.run(tf)

if len(req.prices)==req.hlength:
    run()
