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

rsilength = int(input("rsi length: "))
devlength = int(input("standard deviation length: "))

global row
row = 0
def rsi():
    global row
    prices = req.prices
    g = []
    l = []
    gs = 0
    ls = 0
    for i in range(rsilength):
        if prices[i]['close']-prices[i]['open']>0:
            g.append(prices[i+row]['close']-prices[i+row]['open'])
        if prices[i]['close']-prices[i]['open']<=0:
            l.append(prices[i]['close']-prices[i]['open'])
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

def dev():
    global row
    prices = req.prices
    sum=0
    for i in range(devlength):
        sum+=prices[i]['close']
    diffsum=0
    for i in range(devlength):
        diffsum+=(prices[i]['close']-sum/devlength)**2
    dev = math.sqrt(diffsum/devlength)
    #print(f"dev: {dev}")
    return dev

def run():
    global row
    prices = req.prices
    while row<=len(prices)-20:
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
        analysis.run(prices,rsi(),dev(),row)
        row+=1
        req.run()

req.run()
run()
