import requests
import json
from binance.client import Client

with open('Z:\github/keys.json') as f:
  data = json.load(f)

apikey = data['public']
secretkey = data['secret']

client = Client(apikey, secretkey)
global profit
profit = 0
global tradesum
tradesum = 0
def long(en,prices,rsi):
    print(f"Entered LONG at: {en}")
    #long function
    record(prices,rsi,"short")
def short(en,prices,rsi):
    print(f"Entered SHORT at: {en}")
    #short function
    record(prices,rsi,"short")
def close(ex,pnl,prices,rsi):
    global profit
    global tradesum
    tradesum +=1
    profit+=pnl-.08
    print(f"CLOSED at: {ex} with pNl of: {pnl}")
    print(f"Total pNl: {profit} Total trades: {tradesum}")
    record(prices,rsi,"close")
def record(prices,rsi,type):
    if type == "close":
        timeL = [[prices[row-2]['time']]]
        Jtime = {"values":timeL}
        rsiL = [[round(rsi,2)]]
        Jrsi = {"values":rsiL}
        closeL = [[prices[row-2]['close']]]
        Jclose = {"values":closeL}
        sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'A{row}',valueInputOption='USER_ENTERED',body=Jtime).execute()
        sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'B{row}',valueInputOption='USER_ENTERED',body=Jrsi).execute()
        sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'D{row}',valueInputOption='USER_ENTERED',body=Jclose).execute()
