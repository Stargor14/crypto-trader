import req
import analysis
import math
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
sheet = service.spreadsheets()

rsilength = int(input("rsi length: "))
devlength = int(input("standard deviation length: "))
tf = int(input("input speed: "))

def rsi():
    prices = req.prices
    g = []
    l = []
    gs = 0
    ls = 0
    for i in range(rsilength):
        if prices[i][2]-prices[i][1]>0:
            g.append(prices[i][2]-prices[i][1])
        if prices[i][2]-prices[i][1]<=0:
            l.append(prices[i][2]-prices[i][1])
    for i in g:
        gs+=i
    for i in l:
        ls+=i
    ag = gs/15
    al = abs(ls/15)
    if ag == 0:
        ag = 1
    if al == 0:
        al = 1
    rs = ag/al
    rsi = round((100 - (100/(1+rs))),2)
    rsiL = [[round(rsi,2)]]
    Jrsi = {"values":rsiL}

    sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'B{2}',valueInputOption='USER_ENTERED',body=Jrsi).execute()
    print(f"rsi: {rsi}") #ADD GOOGLE SPREADSHEET FUNCTIONALITY HERE, WILL WRITE RSI VALUE EVERY CANDLE TO SPREADSHEET
    return rsi

def dev():
    prices = req.prices
    sum=0
    for i in range(devlength):
        sum+=prices[i][2]
    diffsum=0
    for i in range(devlength):
        diffsum+=(prices[i][2]-sum/devlength)**2
    dev = math.sqrt(diffsum/devlength)
    #print(f"dev: {dev}")
    return dev

def run():
    while True:
        prices = req.prices
        analysis.run(prices,rsi(),dev())
        req.run(tf)

req.run(tf)

if len(req.prices)==req.hlength:
    run()
