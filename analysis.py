import req
import trader

rsilength = int(input("RSI Length: "))
tf = int(input("Time Frame (in seconds): "))

def loop():
    run()

def run():
    posp = 0
    negp = 0
    for i in range(rsilength):
        if ((req.prices[i+1]/req.prices[i])-1)>0:
            posp += ((req.prices[i+1]/req.prices[i])-1)*100
        if ((req.prices[i+1]/req.prices[i])-1)<0:
            negp += ((req.prices[i+1]/req.prices[i])-1)*100
    if negp==0:
        negp = 1
    if posp==0:
        posp = 1
    #declare averadge gains/losses
    posa = posp/rsilength
    nega = negp/rsilength
    #step 2 rsi
    rsi = 100 - (100/(1+(((posa*(rsilength-1))+(req.prices[1]/req.prices[0]))/((nega*(rsilength-1))+(req.prices[1]/req.prices[0])))))
    print(rsi,req.prices[0], len(req.prices))
    trader.check(rsi)
    req.run(tf)
    loop()

while len(req.prices)<req.hlength:
    req.run(tf)
if len(req.prices)==req.hlength:
    run()
#asd
