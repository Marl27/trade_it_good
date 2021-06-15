import pandas as pd
import mplfinance as mpf
from coinPrice.key_level_finder import range_identification, conn

# global test_keys
# Load data file.
# Plot candlestick.
# Add volume.
# Add moving averages: 3,6,9.
# Save graph to *.png.

# read in your SQL query results using pandas
df = pd.read_sql(
    """     WITH CTE AS (SELECT open_time, open, high, low, close, volume
                FROM xrp_5_minutes_deduped 
                ORDER BY 1 DESC
                LIMIT 700
                ) 
              SELECT open_time, open, high, low, close, volume
                FROM CTE 
                ORDER BY 1
            """,
    conn,
)
df["open_time"] = pd.to_datetime(df["open_time"])
df.set_index("open_time", inplace=True)
df = df.astype(float)
print(df)


df2 = pd.read_sql(
    """With Current_price_getter AS (SELECT "close" AS current_price
            FROM xrp_5_minutes_deduped
            ORDER BY open_time DESC 
            LIMIT 1)
       SELECT kl.price_range_start, kl.price_range_stop, kl.high_count
            , kl.average_of_start_stop, cpg.current_price
            , ((price_range_stop - price_range_start)/price_range_start)*100 AS percentage_diff_from_current_price
        FROM Current_price_getter cpg, high_key_levels kl
        WHERE average_of_start_stop < cpg.current_price
            AND kl.high_count > (SELECT AVG(high_count) FROM high_key_levels)  --(average count of high_count from high_key_levels)
            ORDER BY  kl.high_count DESC, kl.price_range_start DESC 
            LIMIT 10
            """,
    conn,
)
print(df2)
key_levels = df2.loc[:, "average_of_start_stop"]
# key = []
keys = [round(x, 5) for x in key_levels.sort_values()]

# for x in key_levels.sort_values():
#    key.append(round(x, 5))
# print(keys)


mpf.plot(
    df,
    figratio=(30, 15),
    hlines=dict(
        hlines=keys,
        # colors=['g', 'r'],
        linestyle="-.",
    ),
    type="candle",
    style="charles",
    title="XRPUSD",
    ylabel="Price ($)",
    ylabel_lower="Shares \nTraded",
    volume=True,
    # mav=(3, 6, 9),
    figscale=1.5,
    # tight_layout=True
)  # ,
# savefig='test-mplfiance.png')

# mpf.plot(ohlc, hlines=dict(hlines=[0.50422,0.49982],colors=['g','r'],linestyle='-.'))
