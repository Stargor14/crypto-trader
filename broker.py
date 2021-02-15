import json
with open("Z:\github\data.json", "r") as file:
    dataset=json.load(file)
j=0
for i in dataset:
    print(f"rank: {j} RSI length: {i['RSI LENGTH']} Take Profit: {i['TAKE PROFIT']/10} Stop Loss: {i['STOP LOSS']/10} Balance: {round(i['BALANCE'],4)}")
    j+=1
