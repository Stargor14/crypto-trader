import requests
import json
from binance.client import Client
import matplotlib.pyplot as plt

with open('Z:\github/keys.json') as f:
  data = json.load(f)

apikey = data['public']
secretkey = data['secret']

client = Client(apikey, secretkey)
global profit
profit = 0
global tradesum
tradesum = 0
global balance
balance = int(input("Starting balance: "))
global trades
trades=[]
global cooldown
cooldown = 0
global goodlong
goodlong =0
global goodshort
goodshort=0
global badlong
badlong =0
global badshort
badshort=0
def long(en,row):
    print(f"LONG at {en}")
    #long function
    trades.append([row,en,'l'])
def short(en,row):
    print(f"SHORT at {en}")
    #short function
    trades.append([row,en,'s'])
def close(ex,pnl,row,type):
    global balance
    global profit
    global tradesum
    global cooldown
    global goodlong
    global goodshort
    global badshort
    global badlong
    tradesum +=1
    balance=((pnl-.08)/100+1)*balance
    profit+=pnl-.08
    trades.append([row,ex,'c'])
    print(f"CLOSED at {ex} mith pNl of: {pnl}")
    print(f"Total balance: {balance} Total profit: {profit}% Total trades: {tradesum} Good longs: {goodlong} Good shorts: {goodshort} Bad longs: {badlong} Bad shorts: {badshort}")
    if pnl <0:
        cooldown = row+60
        if type == 'l':
            badlong+=1
        else:
            badshort+=1
    if pnl>0:
        if type == 'l':
            goodlong+=1
        else:
            goodshort+=1
