import requests
import json
from binance.client import Client


apikey = "x15G8QtfrUCJG1F7tCahCwyCwxE7a3Mbykg8Q4Uf0Q7QKjB1B3GvCYkfzRUTS96e"
secretkey = "YyATCoS7OwFFAdaqK3UCw0zZLZoz6RWRqarMrHhGi7P08c7Muay8zDWZfV86SxA5"

client = Client(apikey, secretkey)

def openOrder():
    print("shorted!")
def check(rsi):
    print(client.get_exchange_info())
    if rsi>=70:
        openOrder()
