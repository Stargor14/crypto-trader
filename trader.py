'''
maybe make a recomendaion engine? that u can approve the trades of, like ui and can select differnt indicators and use stop losses, trailing stops etc.

historical data? coindesk api, figure out format
calculate % change from entry price to take profit

call price every tick, tick length adjustable?
RSI, MACD, Volatility, MA's
'''
import requests
import json
from binance.client import Client


apikey = "x15G8QtfrUCJG1F7tCahCwyCwxE7a3Mbykg8Q4Uf0Q7QKjB1B3GvCYkfzRUTS96e"
secretkey = "YyATCoS7OwFFAdaqK3UCw0zZLZoz6RWRqarMrHhGi7P08c7Muay8zDWZfV86SxA5"

r = requests.get("https://api.binance.com/api/v3/order/test")
print(r.text)