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
    """    
            SELECT open_time, open, high, low, close, volume
                FROM xrp_5_minutes_deduped 
                ORDER BY 1 --DESC 
                LIMIT 1500
            """,
    conn,
)
df["open_time"] = pd.to_datetime(df["open_time"])
df.set_index('open_time', inplace=True)
df = df.astype(float)
# print(df)


df2 = pd.read_sql(
    """    SELECT *  --, ((average_of_start_stop - ?)/?)*100 AS percentage_diff_from_current_price
            FROM high_key_levels
            --WHERE average_of_start_stop >= ? 
            --WHERE high_count <= 50
            WHERE high_count > 0
            --AND percentage_diff_from_current_price >= 0.5
            ORDER BY high_count DESC, price_range_start
            """,
    conn,
)
key_levels = df2.loc[:, "average_of_start_stop"]
key = []
for x in key_levels.sort_values():
    key.append(round(x, 5))
print(key)


mpf.plot(df,
         figratio=(30, 15),
         hlines=dict(hlines=key,
                     # colors=['g', 'r'],
                     linestyle='-.'),
         type='candle', style='charles',
         title='S&P 500, Nov 2019',
         ylabel='Price ($)',
         ylabel_lower='Shares \nTraded',
         volume=True,
         # mav=(3, 6, 9),
         figscale=1.5,
         # tight_layout=True
         )  # ,
# savefig='test-mplfiance.png')

# mpf.plot(ohlc, hlines=dict(hlines=[0.50422,0.49982],colors=['g','r'],linestyle='-.'))

test_keys = key.copy()
# new_keys = []
# new_keys = test_keys  # sorted(test_keys, reverse=True)

print("key" + str(key))  ##0.48346
print("test_keys" + str(test_keys))
print(len(key))
print(len(test_keys))

# '''
i = 0
# percentage_diff_from_current_price = 0
removeElement = []

while i < len(key):  # 31
    print("**********************************************************")
    print(i)

    if i == len(key) - 1:  # 30th element
        print("breaking***********")
        break
        # '''
    percentage_diff_from_current_price = ((key[i + 1] - key[i]) / key[i]) * 100
    print("before break: " + str(percentage_diff_from_current_price))

    if percentage_diff_from_current_price <= 0.3:

        print("removed After if: ###############" + str(percentage_diff_from_current_price))  # + str(test_keys[i]))
        print(i)
        removeElement.append(i)
        percentage_diff_from_current_price = 0
    else:
        print("NOT Removed")
        percentage_diff_from_current_price = 0
        # '''
    i += 1
# '''


# ((average_of_start_stop - ?)/?)*100 AS percentage_diff_from_current_price


print("key" + str(key))
print("test_keys" + str(test_keys[7]))
print(len(key))
print(len(test_keys))

print("removeElement" + str(removeElement))
print(len(removeElement))
#print(removeElement[6])

for x in range(len(removeElement)):
    test_keys.pop(removeElement[(len(removeElement) - 1) - x])
    print((len(removeElement) - 1) - x)

print("key" + str(key))
print("test_keys" + str(test_keys))
print(len(key))
print(len(test_keys))
#0.45685, 0.48346