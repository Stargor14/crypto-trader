import json
from email.message import EmailMessage
from binance.client import Client

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
