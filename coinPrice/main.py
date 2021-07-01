import sys

# sys.path.insert(0, "C:/Users/Golu/OneDrive - Unai Ltd/Desktop/Stuff/Personal")
sys.path.insert(0, "/home/golu/Desktop/Github")
import config

print(config.API_KEY)

from binance.client import Client
from collection import (
    insert_data,
    unix_timestamp_to_date,
    dateTomorrow,
    dedupe_stuff,
)

# Variables
client = Client(config.API_KEY, config.API_SECRET)  # , tld='us')
dateFrom = unix_timestamp_to_date("13 May, 2018")
dateTo = dateTomorrow()
print("Date from unix_timestamp_to_date() " + dateFrom)

# functionality body
# candlesticks = client.get_historical_klines("XRPUSDT", Client.KLINE_INTERVAL_1DAY, dateFrom, dateTo)
candlesticks = client.get_historical_klines(
    "XRPUSDT", Client.KLINE_INTERVAL_1DAY, dateFrom, dateTo
)
# json_message = json.loads(candles)
# pprint.pprint(json_message)

for candlestick in candlesticks:
    codd_id = insert_data(candlestick)
    # print(
    #     candlestick[0] / 1000,
    #     candlestick[1],
    #     candlestick[2],
    #     candlestick[3],
    #     candlestick[4],
    #     candlestick[5],
    # )
    # print(candlestick)

# candle_data = dedupe_stuff()
print("main.py finished")
from key_level_finder import range_identification
