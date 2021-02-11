import req
import trader

rsilength = int(input("RSI Length: "))
tf = int(input("Time Frame (in seconds): "))

def loop():
    req.run(tf)
    run()

def run():
    gs = 0
    ls = 0
    for i in range(rsilength):
        if (req.prices[i][2]/req.prices[i][1])>=0:
            gs+=(req.prices[i][2]/req.prices[i][1])-1
        if (req.prices[i][2]/req.prices[i][1])<=0:
            ls+=req.prices[i][2]/req.prices[i][1]
    ag1 = gs/14
    al1 = ls/14
    ag = ((ag1*13)+(req.prices[i][2]/req.prices[i][1])-1)/14
    al = ((al1*13)+(req.prices[i][2]/req.prices[i][1])-1)/14
    if ag == 0:
        ag = 1
    if al == 0:
        al = 1
    rs = ag/al
    rsi = 100 - (100/(1+(rs)))
    print(f"RSI: {rsi} Open: {req.prices[0][1]} Price: {req.prices[0][2]}")
    trader.check(rsi)
    loop()

req.run(tf)

if len(req.prices)==req.hlength:
    run()
