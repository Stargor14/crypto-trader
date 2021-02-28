global profit
profit = 0
global tradesum
tradesum = 0
global balance
balance = int(input("Starting balance: "))
global trades
trades=[]
global goodlong
goodlong =0
global goodshort
goodshort=0
global badlong
badlong =0
global badshort
badshort=0
def long(en,row):
    #print(f"LONG at {en}")
    trades.append([row,en,'l'])
def short(en,row):
    #print(f"SHORT at {en}")
    trades.append([row,en,'s'])
def close(ex,pnl,row,type):
    global balance
    global profit
    global tradesum
    global goodlong
    global goodshort
    global badshort
    global badlong
    tradesum +=1
    balance*=((pnl-.08)/100+1)
    profit+=pnl-.08
    trades.append([row,ex,'c'])
    #print(f"CLOSED at {ex} mith pNl of: {pnl}")
    print(f" pNl: {round(pnl-.08,2)} Total balance: {round(balance,2)} Total profit: {round(profit,2)}% G/B L: {goodlong}/{badlong} G/B S: {goodshort}/{badshort}")
    if pnl <0:
        if type == 'l':
            badlong+=1
        else:
            badshort+=1
    if pnl>0:
        if type == 'l':
            goodlong+=1
        else:
            goodshort+=1
