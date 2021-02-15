import req
import analysis
import math
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import pandas
import matplotlib.pyplot as plt
import broker

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'Z:\github\skeys.json'
SPREADSHEET_ID = '1z0_KbA4kywx0P6K08PaK0oCaeRkpts1RO-si7BpFUvs'

credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()
global rsilength
rsilength = int(input("RSI Length: "))
devlength = 100

global row
row = 0
def rsi():
    global row
    global rsilength
    prices = req.prices
    df = pandas.DataFrame(prices)['close']
    delta = df.diff()
    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = up.ewm(span=rsilength).mean()
    roll_down1 = down.abs().ewm(span=rsilength).mean()
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    print(RSI1)
    return RSI1

def macd():
    prices=req.prices
    df = pandas.DataFrame(prices)['close']
    exp1 = df.ewm(span=12, adjust=False).mean()
    exp2 = df.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd,signal

def run():
    global row
    if input("Graph?") != "":
        graph = True
    else:
        graph = False
    prices = req.prices
    macda = macd()[0]
    signala = macd()[1]
    rsia = rsi()
    df = pandas.DataFrame(prices)['close']
    while row<=len(prices)-100:
        analysis.run(prices,rsia[row],macda[row],signala[row],row)
        row+=1
    if row==len(prices)-99 and graph ==True:
        trades = broker.trades
        macda.plot(label='BTC MACD', color='g')
        rsia.plot(label='RSI',color='b')
        ax = signala.plot(label='Signal Line', color='r')
        df.plot(ax=ax, secondary_y=True, label='BTC')
        ax.set_ylabel('MACD')
        ax.right_ax.set_ylabel('Price $')
        ax.set_xlabel('CANDLE')
        lines = ax.get_lines() + ax.right_ax.get_lines()
        ax.legend(lines, [l.get_label() for l in lines], loc='upper left')
        x_list = [x for [x, y,z] in trades]
        y_list = [y for [x, y,z] in trades]
        z_list = [z for [x, y,z] in trades]
        for i in range(len(x_list)):
            if z_list[i]=='s':
                plt.scatter(x_list[i], y_list[i],color='r')
            if z_list[i]=='l':
                plt.scatter(x_list[i], y_list[i],color='g')
            if z_list[i]=='c':
                plt.scatter(x_list[i], y_list[i],color='b')
        plt.show()
req.run()
run()
