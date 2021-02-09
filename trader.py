import requests
import json
from binance.client import Client
import rsi

apikey = "x15G8QtfrUCJG1F7tCahCwyCwxE7a3Mbykg8Q4Uf0Q7QKjB1B3GvCYkfzRUTS96e"
secretkey = "YyATCoS7OwFFAdaqK3UCw0zZLZoz6RWRqarMrHhGi7P08c7Muay8zDWZfV86SxA5"

def openOrder(buy):
    if buy == False:
        print("sold!")

while True:
    if rsi.rsi >=70:
        openOrder(False)
    
