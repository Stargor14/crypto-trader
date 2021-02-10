import requests
import json
from binance.client import Client


apikey = "x15G8QtfrUCJG1F7tCahCwyCwxE7a3Mbykg8Q4Uf0Q7QKjB1B3GvCYkfzRUTS96e"
secretkey = "YyATCoS7OwFFAdaqK3UCw0zZLZoz6RWRqarMrHhGi7P08c7Muay8zDWZfV86SxA5"

client = Client(apikey, secretkey)

def openOrder():
    print("shorted!")
def check(rsi):
    if rsi>=70:
        openOrder()

'''
candles = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
for i in candles:
    open = float(i[1])
    close = float(i[4])
    print(f"Open: {open} Close: {close} Difference: {close-open} Difference %: {((close/open)-1)*100}")
'''
