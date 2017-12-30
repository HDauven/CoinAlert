from bittrex.bittrex import Bittrex
from deepdiff import DeepDiff
from time import time, sleep
import dotenv
import pprint
pp = pprint.PrettyPrinter(width=41, compact=True)

dotenv.load()

key = dotenv.get('bittrex_key')
secret = dotenv.get('bittrex_secret')
interval = dotenv.get('polling_interval')

my_bittrex = Bittrex(key, secret)  # or defaulting to v1.1 as Bittrex(None, None)

markets = my_bittrex.get_markets()['result']
currencies = my_bittrex.get_currencies()['result']

pp.pprint(len(markets))
pp.pprint(len(currencies))

while True:
    print('Tick')
    temp_markets = my_bittrex.get_markets()['result']
    temp_currencies = my_bittrex.get_currencies()['result']
    new_markets = DeepDiff(markets, temp_markets, ignore_order=True)
    new_currencies = DeepDiff(currencies, temp_currencies, ignore_order=True)
    if 'iterable_item_added' in new_markets:
        print('New market added!')
        for market in new_markets['iterable_item_added']:
            print("New Market: {}".format(market))
    pp.pprint(new_markets)
    pp.pprint(new_currencies)
    sleep(interval - time() % interval)
