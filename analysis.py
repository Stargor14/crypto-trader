import req
import trader

rsilength = int(input("RSI Length: "))
tf = int(input("Time Frame (in seconds): "))

def loop():
    run()

def run():
    poss = 0
    negs = 0
    for i in range(1,rsilength):
        if ((req.prices[i][2]/req.prices[i][1])-1)*100>=0:
            poss += (((req.prices[i][2]/req.prices[i][1])-1)*100)
        if ((req.prices[i][2]/req.prices[i][1])-1)*100<=0:
            negs += (((req.prices[i][2]/req.prices[i][1])-1)*100)
    nega = negs/rsilength
    posa = poss/rsilength
    currdiff = ((req.prices[0][2]/req.prices[0][1])-1)*100
    if currdiff>=0:
        rsi = 100 -(100/(1+((posa+currdiff)/((-1)*(nega)))))
    if currdiff<=0:
        rsi = 100 -(100/(1+((posa)/((-1)*(nega+currdiff)))))
    av = 0
    for i in range(5):
        av+=req.prices[i][2]
    av = av/5
    if av>req.prices[0][2]:
        print(av,req.prices[0][2],"lower", rsi)
    if av<req.prices[0][2]:
        print(av,req.prices[0][2],"higher", rsi)
    #print(f"RSI: {rsi} Price: {req.prices[0][2]} Price diff this candle: {((req.prices[0][2]/req.prices[0][1])-1)*100}%")
    trader.check(rsi)
    req.run(tf)
    loop()

req.run(tf)
if len(req.prices)==req.hlength:
    run()
