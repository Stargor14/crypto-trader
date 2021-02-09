import req
while len(req.prices)<14:
    req.run(1)
while len(req.prices)==14:
    posp = 0
    negp = 0
    for i in range(10):
        if ((req.prices[i+1]/req.prices[i])-1)>0:
            posp += ((req.prices[i+1]/req.prices[i])-1)*100
        if ((req.prices[i+1]/req.prices[i])-1)<0:
            negp += ((req.prices[i+1]/req.prices[i])-1)*100
    if negp==0:    
        negp = 1
    if posp==0:    
        posp = 1
    #step 1 rsi        
    rsi = 100 - (100/(1+((posp/10)/(negp/10))))
    print(rsi)
    req.run(1)