import sys

# sys.path.insert(0, "C:/Users/Golu/OneDrive - Unai Ltd/Desktop/Stuff/Personal")
sys.path.insert(0, "/home/golu/Desktop/Github")
import config
from binance.client import Client
from coinPrice.collection import create_table, conn


# Variables
client = Client(config.API_KEY, config.API_SECRET)  # , tld='us')

create_table()
cursor = conn.cursor()
'''
cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY, 
                symbol TEXT NOT NULL UNIQUE, 
                price TEXT NOT NULL);
""")
'''
symbols = client.get_all_tickers()
count = 0
for symbol in symbols:
    print(symbol['symbol'])
    print(symbol['price'])
    count += 1

#     try:
#         cursor.execute("""
#                 INSERT INTO assets (symbol, price)
#                 VALUES (?, ?)
#             """, (symbol['symbol'], symbol['price']))
#         print("INTO THE TABLE")
#     except Exception as e:
#         print(e)
#         print(symbol)
#
# conn.commit()

print(type(symbols))
print(len(symbols))
print(count)
