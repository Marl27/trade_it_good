import backtrader as bt
import datetime
# from strategies import TestStrategy
from key_level_strategy import Key_level_strategy
import pandas as pd
import matplotlib.dates as mpl_dates
import mplfinance as mpf
from coinPrice.key_level_finder import range_identification, conn

cerebro = bt.Cerebro()
cerebro.broker.setcash(200.0)

# Create a Data Feed
# data = bt.feeds.YahooFinanceCSVData(
#     dataname='Oracle.csv',
#     # Do not pass values before this date
#     fromdate=datetime.datetime(2000, 1, 1),
#     # Do not pass values after this date
#     todate=datetime.datetime(2000, 12, 31),
#     reverse=False)

df = pd.read_sql("""
            SELECT open_time, open, high, low, close, volume
                FROM xrp_5_minutes_deduped 
                ORDER BY 1 -- DESC 
                --LIMIT 15000
                """, conn)  # , index_col=['open_time'] , parse_dates=['open_time']

# df["open_time"] = pd.to_datetime(df["open_time"])
# df.set_index('open_time', inplace=True)
df["open_time"] = pd.to_datetime(df["open_time"])
df.set_index('open_time', inplace=True)
df = df.astype(float)

# print(df)


data = bt.feeds.PandasData(dataname=df)  # , datetime=1)

# Add the Data Feed to Cerebro
cerebro.adddata(data)
# cerebro.addsizer(bt.sizers.FixedSize, stake=10000)
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
cerebro.broker.setcommission(commission=0.001)
cerebro.addstrategy(Key_level_strategy)
# strats = cerebro.optstrategy(Key_level_strategy, num_opening_bars=[15, 30, 60])


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot(style="candle")
