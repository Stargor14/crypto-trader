class live:
    def __init__(self):
        self.entry = 0
        self.exit = 0
        self.balance = 100
    def sell():
        return
    def buy():
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
