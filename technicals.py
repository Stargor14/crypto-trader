import req
import analysis
import math
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'Z:\github\skeys.json'
SPREADSHEET_ID = '1z0_KbA4kywx0P6K08PaK0oCaeRkpts1RO-si7BpFUvs'

credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()
global rsilength
rsilength = 14
devlength = 100

global row
row = 0
def rsi():
    global row
    global rsilength
    prices = req.prices
    g = []
    l = []
    gs = 0
    ls = 0
    for i in range(rsilength):
        if prices[i+row]['close']-prices[i+row]['open']>0:
            g.append(prices[i+row]['close']-prices[i+row]['open'])
        if prices[i+row]['close']-prices[i+row]['open']<=0:
            l.append(prices[i+row]['close']-prices[i+row]['open'])
    for i in g:
        gs+=i
    for i in l:
        ls+=i
    ag = gs/rsilength
    al = abs(ls/rsilength)
    if ag == 0:
        ag = 1
    if al == 0:
        al = 1
    rs = ag/al
    rsi = round((100 - (100/(1+rs))),2)
    #print(f"rsi: {rsi}")
    return rsi

def sma(len,target):
    prices = req.prices
    sum=0
    for i in range(len):
        sum+=prices[target]['close']
    sma = sum/len
    return sma

def ema(len,target):
    prices = req.prices
    ema =[]
    n=0
    for i in reversed(range(len)):
        if i == len-1:
            ema.append(sma(len,target+i))
            n+=1
        else:
        # multiplier: (2 / (length + 1))
        # EMA: (close * multiplier) + ((1 - multiplier) * EMA(previous))
            multiplier = 2 / (len + 1)
            ema.append((prices[i+target]['close'] * multiplier) + (ema[n-1]*(1 - multiplier)))
            n+=1
    return ema[len-1]

def macd(target):
    ema26 = ema(26,target)
    ema12 = ema(12,target)
    macd = ema12 - ema26
    return macd

def sigsma(macd):
    sum=0
    for i in range(9):
        sum+=macd[i+8]
    sma = sum/9
    return sma

def signal(macd):
    ema=[]
    n=0
    for i in reversed(range(9)):
        if i == 8:
            ema.append(sigsma(macd))
            n+=1
        else:
        # multiplier: (2 / (length + 1))
        # EMA: (close * multiplier) + ((1 - multiplier) * EMA(previous))
            multiplier = 2 / (9 + 1)
            ema.append((macd[i] * multiplier) + (ema[n-1]*(1 - multiplier)))
            n+=1
    return ema[8]

def run():
    global row
    prices = req.prices
    while row<=len(prices)-100:
        '''
        timeL = [[prices[row-2]['time']]]
        Jtime = {"values":timeL}
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
        '''
        m=[]
        for i in range(17):
            m.append(macd(i))
        analysis.run(prices,rsi(),macd(row),signal(m),row)
        row+=1
        req.run()

req.run()
run()
