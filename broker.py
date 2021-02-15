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
def long(en,row):
    print(f"Entered LONG at: {en}")
    #long function
    trades.append([row,en,'l'])
def short(en,row):
    print(f"Entered SHORT at: {en}")
    #short function
    trades.append([row,en,'s'])
def close(ex,pnl,row):
    global balance
    global profit
    global tradesum
    tradesum +=1
    balance=((pnl-.08)/100+1)*balance
    profit+=pnl-.08
    trades.append([row,ex,'c'])
    print(f"CLOSED at: {ex} with pNl of: {pnl-.08}")
    print(f"Total balance: {balance} Total profit: {profit}% Total trades: {tradesum}")
