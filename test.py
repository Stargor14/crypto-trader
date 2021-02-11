orderbook = {'buy price': 1000, 'sell price':1100, "qty":100}
def calc(book):
    return (book['sell price']-book['buy price'])*book['qty']
print(calc(orderbook))
