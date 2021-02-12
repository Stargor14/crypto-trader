import math
prices=[]
sum=0
for price in prices:
    sum+=price
diffsum=0
for price in prices:
    diffsum+=(price-sum/len(prices))**2
var = math.sqrt(diffsum/len(prices))
print(var)
