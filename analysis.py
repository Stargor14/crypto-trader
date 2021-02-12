import trader
def run(prices,rsi,dev):
    if rsi>=80:
        trader.short()
        entry = prices[0][2]
    if rsi<=30:
        pass
