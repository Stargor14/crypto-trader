import requests
import json
import smtplib
import os
from email.message import EmailMessage
from binance.client import Client
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'Z:\github\skeys.json'
SPREADSHEET_ID = '1z0_KbA4kywx0P6K08PaK0oCaeRkpts1RO-si7BpFUvs'

credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
global sheet
sheet = service.spreadsheets()

with open('Z:\github\keys.json') as f:
  data = json.load(f)

apikey = data['public']
secretkey = data['secret']
global client
client = Client(apikey, secretkey)
global Email_Adress
Email_Adress = 'andy.btc.profit@gmail.com'
global Email_Password
Email_Password = 'sgijlrmqtkskkabi'

def record(prices,rsi,type,pnl):
    with open('row.json','r') as f:
      data = json.load(f)
    row = data['row']
    timeL = [[prices[0]['time']]]
    Jtime = {"values":timeL}
    rsiL = [[round(rsi,2)]]
    Jrsi = {"values":rsiL}
    closeL = [[prices[0]['close']]]
    Jclose = {"values":closeL}
    typeL = [[type]]
    Jtype = {"values":typeL}
    pnlL = [[pnl]]
    Jpnl = {"values":pnlL}
    sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'A{row}',valueInputOption='USER_ENTERED',body=Jtime).execute()
    sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'B{row}',valueInputOption='USER_ENTERED',body=Jrsi).execute()
    sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'C{row}',valueInputOption='USER_ENTERED',body=Jclose).execute()
    sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'D{row}',valueInputOption='USER_ENTERED',body=Jtype).execute()
    if type == "close":
        sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'E{row}',valueInputOption='USER_ENTERED',body=Jpnl).execute()
    row+=1
    with open('row.json','w') as f:
      json.dump({"row":row},f)

def long(en,prices,rsi):
    global client
    balance = client.futures_account_balance()[0]['balance']
    print(balance)
    quantity = round((float(balance)/prices[0]['close'])*1.5,3)
    print(f"Entered LONG at: {en}")
    client.futures_create_order(symbol='BTCUSDT',side="BUY",positionSide='LONG',type="MARKET",quantity=quantity)
    record(prices,rsi,"long",0)

def short(en,prices,rsi):
    global client
    print(f"Entered SHORT at: {en}")
    balance = client.futures_account_balance()[0]['balance']
    print(balance)
    quantity = round((float(balance)/prices[0]['close']*1.5),3)
    client.futures_create_order(symbol='BTCUSDT',side="SELL",positionSide='SHORT',type="MARKET",quantity=quantity)
    record(prices,rsi,"short",0)

def close(ex,pnl,prices,rsi,type):
    global Email_Adress
    global Email_Password
    global message
    print(f"CLOSED at: {ex} with pNl of: {pnl}")
    info = client.futures_position_information(symbol='BTCUSDT')
    if type == 's':
        client.futures_create_order(symbol='BTCUSDT',side="BUY",positionSide='SHORT',type="MARKET",quantity=float(info[0]['positionAmt']))
    if type == 'l':
        client.futures_create_order(symbol='BTCUSDT',side="SELL",positionSide='LONG',type="MARKET",quantity=float(info[0]['positionAmt']))
    for email in emailList:
        msg = EmailMessage()
        msg['Subject'] = 'Michaels New Weight!!'
        msg['From'] = Email_Adress
        msg['to'] = email
        msg.set_content(f"{message}")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(Email_Adress, Email_Password)
            smtp.send_message(msg)
    record(prices,rsi,"close",pnl)
