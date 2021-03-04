from binance.client import Client
with open('keys.json','r') as r:
    data  = json.load(r)
    api_key = data['public']
    api_secret = data['secret']

global client
client = Client(api_key, api_secret)

class live:
    def __init__(self):
        self.entry = 0
        self.exit = 0
        self.balance = 100
    def enter(seld,price,type):
        self.entry = price
        if type == "buy":
            global client
            balance = client.futures_account_balance()[0]['balance']
            print(balance)
            quantity = round((float(balance)/price)*1.5,3)
            print(f"Entered LONG at: {price}")
            client.futures_create_order(symbol='BTCUSDT',side="BUY",type="MARKET",quantity=quantity)
        if type == "sell":
            global client
            balance = client.futures_account_balance()[0]['balance']
            print(balance)
            quantity = round((float(balance)/price)*1.5,3)
            print(f"Entered short at: {price}")
            client.futures_create_order(symbol='BTCUSDT',side="SELL",type="MARKET",quantity=quantity)
        return
    def close(self,type): #add stop loss limit order maybe?
        self.exit = price
        global client
        info = client.futures_position_information(symbol='BTCUSDT')
        if type == 'sell':
            client.futures_create_order(symbol='BTCUSDT',side="BUY",type="MARKET",quantity=float(info[0]['positionAmt']))
        if type == 'buy':
            client.futures_create_order(symbol='BTCUSDT',side="SELL",type="MARKET",quantity=float(info[0]['positionAmt']))
        return

class backtester:
    def __init__(self):
        self.entry = 0
        self.exit = 0
        self.balance = 100
        self.trades = 0
        return
    def enter(self, price):
        self.entry = price
        return
    def close(self,price,type):
        self.exit = price
        if(type == "sell"):
            self.balance*=self.entry/self.exit-.001
            self.trades+=1
        if(type == "buy"):
            self.balance*=self.exit/self.entry-.001
            self.trades+=1
        return
