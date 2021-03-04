class macd:
    def check(macd,signal,pnl,stopLoss):
        if (pnl<=-stopLoss):
            return "close"
        if (macd > signal):
            return "buy"
        if (macd < signal):
            return "sell"
class rsi:
    rsiHigh = 70
    rsiLow = 30
    value = 25
    confidence = 0
    def check(rsi):
        if(rsi<rsiLow):
            return "buy"
        if(rsi>rsiHigh):
            return "sell"

class macdrsi:
    rsiHigh = 70
    rsiLow = 30
    value = 25
    confidence = 0
    def check(macd,signal,rsi,postion):
        if (macd.check(macd,signal) == "buy" and rsi<rsiLow):
            return "buy"
        if (macd.check(macd,signal) == "sell" and rsi>rsiHigh):
            return "sell"
