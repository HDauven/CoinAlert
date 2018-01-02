from binance.client import Client
from bittrex.bittrex import Bittrex
from deepdiff import DeepDiff
from time import time, sleep
import dotenv
import pprint
import datetime
from telegram.ext import Updater, CommandHandler

pp = pprint.PrettyPrinter(width=41, compact=True)

dotenv.load()

binance_api_key = dotenv.get('binance_api_key')
binance_api_secret = dotenv.get('binance_api_secret')

binance_client = Client(binance_api_key, binance_api_secret)
tickers = binance_client.get_all_tickers()
t1 = [{'symbol': ticker['symbol']} for ticker in tickers]

bittrex_api_key = dotenv.get('bittrex_api_key')
bittrex_api_secret = dotenv.get('bittrex_api_secret')
interval = dotenv.get('polling_interval')

my_bittrex = Bittrex(bittrex_api_key, bittrex_api_secret)
currencies = my_bittrex.get_currencies()['result']
c1 = [{'Currency': currency['Currency'], 'CurrencyLong': currency['CurrencyLong']} for currency in currencies]
markets = my_bittrex.get_markets()['result']
m1 = [{'MarketName': market['MarketName'], 'MarketCurrencyLong': market['MarketCurrencyLong']} for market in markets]

updater = Updater(token=dotenv.get('telegram_bot'))
dispatcher = updater.dispatcher

dispatcher.bot.send_message(dotenv.get('telegram_group'), 'Waking up...')

dispatcher.bot.send_message(dotenv.get('telegram_group'), '{} tickers on Binance'.format(len(tickers)))
dispatcher.bot.send_message(dotenv.get('telegram_group'), '{} markets on Bittrex'.format(len(markets)))
dispatcher.bot.send_message(dotenv.get('telegram_group'), '{} currencies on Bittrex'.format(len(currencies)))


def check_for_changes(command, result_list, value_of_interest, value_of_interest_long, identifier, exchange):
    if command in result_list:
        print('Changes found on {}'.format(exchange))
        for item in result_list[command]:
            if not value_of_interest_long:
                message = 'New {} found on {}: {}'.format(identifier, exchange, result_list[command][item][value_of_interest])
                print(message)
                dispatcher.bot.send_message(dotenv.get('telegram_group'), message)
            else:
                message = 'New {} found on {}: {} - {}'.format(identifier, exchange,
                                                           result_list[command][item][value_of_interest],
                                                           result_list[command][item][value_of_interest_long])
                print(message)
                dispatcher.bot.send_message(dotenv.get('telegram_group'), message)


while True:
    print('Checked on {}'.format(datetime.datetime.now()))
    temp_currencies = my_bittrex.get_currencies()['result']
    c2 = [{'Currency': currency['Currency'], 'CurrencyLong': currency['CurrencyLong']} for currency in temp_currencies]
    temp_markets = my_bittrex.get_markets()['result']
    m2 = [{'MarketName': market['MarketName'], 'MarketCurrencyLong': market['MarketCurrencyLong']} for market in temp_markets]
    temp_tickers = binance_client.get_all_tickers()
    t2 = [{'symbol': ticker['symbol']} for ticker in temp_tickers]

    new_currencies = DeepDiff(c1, c2, ignore_order=True)
    new_markets = DeepDiff(m1, m2, ignore_order=True)
    new_tickers = DeepDiff(t1, t2, ignore_order=True)

    check_for_changes('iterable_item_added', new_currencies, 'Currency', 'CurrencyLong', 'currency', 'Bittrex')
    check_for_changes('iterable_item_added', new_markets, 'MarketName', 'MarketCurrencyLong', 'market', 'Bittrex')
    check_for_changes('iterable_item_added', new_tickers, 'symbol', '', 'ticker', 'Binance')

    c1 = c2
    m1 = m2
    t1 = t2

    pp.pprint(new_markets)
    pp.pprint(new_currencies)
    pp.pprint(new_tickers)
    sleep(interval - time() % interval)

# def main():
#
#
#
# if __name__ == '__main__':
#     main()
