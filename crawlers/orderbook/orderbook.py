import copy
import json
import ssl
import time
import websocket


class OrderBook(object):

    BIDS = 'bid'
    ASKS = 'ask'

    def __init__(self, limit=10):

        self.limit = limit

        # two dictionaries to store current bids and offers
        self.bids = {}
        self.asks = {}

        self.bids_sorted = []
        self.asks_sorted = []

    def insert(self, price, amount, direction):

        # if the amount of a price is 0, delete it from the dictionary
        if direction == self.BIDS:
            if amount == 0:
                if price in self.bids:
                    del self.bids[price]
            else: 
                self.bids[price] = amount
        elif direction == self.ASKS:
            if amount == 0:
                if price in self.ASKS:
                    del self.asks[price]
            else:
                self.asks[price] = amount
        else:
            print("Unknown direction {}".format(direction))

    def sort_and_truncate(self):
        # sort
        self.bids_sorted = sorted([(price, amount) for price, amount in self.bids.items()], reverse=True)
        self.asks_sorted = sorted([(price, amount) for price, amount in self.asks.items()])

        # truncate
        self.bids_sorted = self.bids_sorted[:self.limit]
        self.asks_sorted = self.asks_sorted[:self.limit]

        self.bids = dict(self.bids_sorted)
        self.asks = dict(self.asks_sorted)

    def get_copy(self):
        return copy.deepcopy(self.bids_sorted), copy.deepcopy(self.asks_sorted)


class Crawler:
    def __init__(self, symbol, filename):
        self.orderbook = OrderBook(limit = 5)
        self.filename = filename

        self.ws = websocket.WebSocketApp('wss://api.gemini.com/v1/marketdata/{}'.format(symbol), \
            on_message = lambda ws, message: self.on_message(message))
        self.ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})

    def on_message(self, message):
        # processing the recieved data then pip to orderbook
        data = json.loads(message)
        for event in data['events']:
            price, amount, direction = float(event['price']), float(event['remaining']), event['side']
            self.orderbook.insert(price, amount, direction)

        # sort the orderbook, select what we need
        self.orderbook.sort_and_truncate()

        # output to a file
        with open(self.filename, 'a+') as f:
            bids, asks = self.orderbook.get_copy()
            output = {
                'bids': bids,
                'asks': asks,
                'ts': int(time.time() * 1000)
            }
            f.write(json.dumps(output) + '\n')


if __name__ == '__main__':
    # symbol can be "BTCUSD", "ETHBTC", etc
    crawler = Crawler(symbol='ETHBTC', filename='ETHBTC.txt')
