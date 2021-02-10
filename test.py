from binance.client import Client

apikey = "x15G8QtfrUCJG1F7tCahCwyCwxE7a3Mbykg8Q4Uf0Q7QKjB1B3GvCYkfzRUTS96e"
secretkey = "YyATCoS7OwFFAdaqK3UCw0zZLZoz6RWRqarMrHhGi7P08c7Muay8zDWZfV86SxA5"
global client
client = Client(apikey, secretkey)
kline = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=2)
a = [kline[0][0], float(kline[0][1]), float(kline[0][4])]
for i in kline:
    print(i[0],i[1],i[4])
