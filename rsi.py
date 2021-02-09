import req
while len(req.prices)<60:
    req.run(1)
while len(req.prices)==60:
    posp = 0
    negp = 0
    for i in range(50):
        if ((req.prices[i+1]/req.prices[i])-1)>0:
            posp += ((req.prices[i+1]/req.prices[i])-1)*100
        if ((req.prices[i+1]/req.prices[i])-1)<0:
            negp += ((req.prices[i+1]/req.prices[i])-1)*100
    if negp==0:    
        negp = 1
    if posp==0:    
        posp = 1      
    posa = posp/50 
    nega = negp/50
    #step 2 rsi
    rsi = 100 - (100/(1+(((posa*49)+(req.prices[1]/req.prices[0]))/((nega*49)+(req.prices[1]/req.prices[0])))))
    print(rsi,req.prices[0])
    req.run(1)