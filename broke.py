from enum import Enum
class types(Enum):
    Long = 1
    Short = 2
    Closed = 3

class paper:
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
        self.entry = 1
        self.exit = 1
        self.balance = 100
        self.trades = 0
        return
    def enter(self, price):
        self.entry = price
        return
    def close(self, price,type):
        self.exit = price
        if(type == "sell"):
            self.balance*=self.entry/self.exit-.0008
            self.trades+=1
        if(type == "buy"):
            self.balance*=self.exit/self.entry-.0008
            self.trades+=1
        return
