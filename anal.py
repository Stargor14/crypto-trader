class macd:
    periodFast = 12
    periodSlow = 26
    value = 25
    confidence = 0
    def check(macd,signal):
        if (macd > signal):
            return macd,signal
        if (macd < signal):
            return macd,signal

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
    def check(macd,signal,rsi):
        if (macd.check() == "buy" and rsi>rsiHigh):
            return "buy"
        if (macd.check() == "sell" and rsi<rsiLow):
            return "sell"
