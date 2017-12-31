from bittrex.bittrex import Bittrex
from deepdiff import DeepDiff
from time import time, sleep
import dotenv
import pprint
from telegram.ext import Updater, CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

pp = pprint.PrettyPrinter(width=41, compact=True)

dotenv.load()

key = dotenv.get('bittrex_key')
secret = dotenv.get('bittrex_secret')
interval = dotenv.get('polling_interval')

my_bittrex = Bittrex(key, secret)  # or defaulting to v1.1 as Bittrex(None, None)

markets = my_bittrex.get_markets()['result']
currencies = my_bittrex.get_currencies()['result']

updater = Updater(token=dotenv.get('telegram_bot'))
dispatcher = updater.dispatcher

pp.pprint(len(markets))
dispatcher.bot.send_message(dotenv.get('telegram_group'), '{} markets on Bittrex'.format(len(markets)))
pp.pprint(len(currencies))
dispatcher.bot.send_message(dotenv.get('telegram_group'), '{} currencies on Bittrex'.format(len(currencies)))


while True:
    print('Tick')
    temp_markets = my_bittrex.get_markets()['result']
    temp_currencies = my_bittrex.get_currencies()['result']
    new_markets = DeepDiff(markets, temp_markets, ignore_order=True)
    new_currencies = DeepDiff(currencies, temp_currencies, ignore_order=True)
    if 'iterable_item_added' in new_markets:
        print('New market added!')
        dispatcher.bot.send_message(dotenv.get('telegram_group'), 'New market(s) added to Bittrex!')
        for market in new_markets['iterable_item_added']:
            print("New market: {}".format(market))
            dispatcher.bot.send_message(dotenv.get('telegram_group'), 'New market: {}'.format(market))

    if 'iterable_item_added' in new_currencies:
        print('New currency added!')
        dispatcher.bot.send_message(dotenv.get('telegram_group'), 'New currency(ies) added to Bittrex!')
        for currency in new_currencies['iterable_item_added']:
            print("New currency: {}".format(currency))
            dispatcher.bot.send_message(dotenv.get('telegram_group'), 'New currency: {}'.format(currency))

    pp.pprint(new_markets)
    pp.pprint(new_currencies)
    sleep(interval - time() % interval)

# def main():
#
#
#
# if __name__ == '__main__':
#     main()
