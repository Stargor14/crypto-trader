class macd:
    periodFast = 12
    periodSlow = 26
    value = 25
    confidence = 0
    def check(macd,check,position):
        print("check")
        if macd > signal and position == "short":
            return "buy"
        if macd < signal and position == "long":
            return "sell"

class rsi:
    rsiHigh = 70
    rsiLow = 30
    value = 25
    confidence = 0
    def check(rsi):
        if rsi<rsiLow:
            return "buy"
        if rsi>rsiHigh:
            return "sell"

class macdrsi:
    rsiHigh = 70
    rsiLow = 30
    value = 25
    confidence = 0
    def check(macd,):
        if macd.check() == "buy" and rsi>rsiHigh:
            confidence
        if macd.check() == "sell" and rsi<rsiLow:
            return "sell"

anals = [macd(),rsi(),macdrsi()]
class confidence:
    def check(macd, signal, rsi):
        for anal in anals:
            confidence+=
        if confidence==100:
            return "buy"
        if confidence==75:
            return "buy"
        if confidence==50:
            return "buy"
        if confidence==25:
            return "buy"
        if confidence==0:
            return
        if confidence==-25:
            return "sell"
        if confidence==-50:
            return "sell"
        if confidence==-75:
            return "sell"
        if confidence==-100:
            return "sell"

print(macd.check())
