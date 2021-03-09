import sys

sys.path.insert(0, "C:/Users/Golu/Desktop/Stuff/Personal")
import config

print(config.API_KEY)

from binance.client import Client
from coinPrice.collection import (
    insert_data,
    unix_timestamp_to_date,
    dateTomorrow,
    dedupe_stuff,
)


# Variables
client = Client(config.API_KEY, config.API_SECRET)  # , tld='us')
dateFrom = unix_timestamp_to_date()
dateTo = dateTomorrow()
print("Date from unix_timestamp_to_date() " + dateFrom)


# functionality body
candlesticks = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, dateFrom, dateTo
)
# json_message = json.loads(candles)
# pprint.pprint(json_message)

for candlestick in candlesticks:

    codd_id = insert_data(candlestick)
    print(
        candlestick[0] / 1000,
        candlestick[1],
        candlestick[2],
        candlestick[3],
        candlestick[4],
        candlestick[5],
    )
    # print(candlestick)


candle_data = dedupe_stuff()
