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

global row
row = 2
def rsi():
    global row
    prices = req.prices
    g = []
    l = []
    gs = 0
    ls = 0
    for i in range(rsilength):
        if prices[i+row-2]['close']-prices[i+row-2]['open']>0:
            g.append(prices[i+row-2]['close']-prices[i+row-2]['open'])
        if prices[i+row-2]['close']-prices[i+row-2]['open']<=0:
            l.append(prices[i+row-2]['close']-prices[i+row-2]['open'])
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
    #print(f"rsi: {rsi}") #ADD GOOGLE SPREADSHEET FUNCTIONALITY HERE, WILL WRITE RSI VALUE EVERY CANDLE TO SPREADSHEET
    return rsi

def dev():
    global row
    prices = req.prices
    sum=0
    for i in range(devlength):
        sum+=prices[i+row-2]['close']
    diffsum=0
    for i in range(devlength):
        diffsum+=(prices[i+row-2]['close']-sum/devlength)**2
    dev = math.sqrt(diffsum/devlength)
    #print(f"dev: {dev}")
    return dev

def run():
    global row
    while row<=1000:
        prices = req.prices
        rsiL = [[round(rsi(),2)]]
        Jrsi = {"values":rsiL}
        openL = [[prices[row-2]['open']]]
        Jopen = {"values":openL}
        closeL = [[prices[row-2]['close']]]
        Jclose = {"values":closeL}
        lowL = [[prices[row-2]['low']]]
        Jlow = {"values":lowL}
        highL = [[prices[row-2]['high']]]
        Jhigh = {"values":highL}

        sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'A{row}',valueInputOption='USER_ENTERED',body=Jtime).execute()
        sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'B{row}',valueInputOption='USER_ENTERED',body=Jrsi).execute()
        sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'C{row}',valueInputOption='USER_ENTERED',body=Jopen).execute()
        sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'D{row}',valueInputOption='USER_ENTERED',body=Jclose).execute()
        sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'E{row}',valueInputOption='USER_ENTERED',body=Jlow).execute()
        sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'F{row}',valueInputOption='USER_ENTERED',body=Jhigh).execute()

        row+=1
        analysis.run(prices,rsi(),dev())
        req.run(tf)

req.run(tf)

if len(req.prices)==req.hlength:
    run()
