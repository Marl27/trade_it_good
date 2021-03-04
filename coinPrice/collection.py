# import sqlite3
from coinPrice.db_utils import db_connect
from datetime import datetime, timedelta

conn = db_connect()


def create_table():
    cursor = conn.cursor()
    #### Notice the use of the ROWID
    try:
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS xrp_5_minutes ( 
                    open_time TEXT,
                    open TEXT,
                    high TEXT,
                    low TEXT,
                    close TEXT,
                    volume TEXT,
                    close_time TEXT,
                    quote_asset_volume TEXT,
                    number_of_trades TEXT,
                    taker_buy_base_asset_volume TEXT,
                    taker_buy_quote_asset_volume TEXT,
                    ignore TEXT);
                            
            DROP TABLE IF EXISTS high_key_levels;
            CREATE TABLE high_key_levels(
                    number_of_ranges INTEGER NOT NULL,
                    price_range_start NUMERIC(6,5) NOT NULL,
                    price_range_stop NUMERIC(6,5) NOT NULL,
                    high_count INTEGER NOT NULL);
                            """
        )
        print(conn.total_changes)
        conn.commit()
    except:
        conn.rollback()
        raise RuntimeError("Uh oh, an error occurred while Creating tables...")






def insert_data(data):
    cursor = conn.cursor()

    # if open_time already exists use update method here based on the logic given in update_data() method.
    # update_data()
    # print(conn.total_changes)
    try:
        sql = """
           INSERT INTO xrp_5_minutes (open_time, open, high, low, close, volume, close_time, quote_asset_volume, 
           number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(
            sql,
            (
                data[0] / 1000,
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6] / 1000,
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
            ),
        )
        conn.commit()
    except:
        conn.rollback()
        raise RuntimeError("Uh oh, an error occurred while inserting...")
    # print("----Insert Finished----")
    return cursor.lastrowid


def update_data(data):
    # will update the existing records based on (open_time, open, high,
    # low, close and close_time)to avoid duplicate records
    cursor = conn.cursor()
    try:
        sql = """
           UPDATE xrp_5_minutes 
           SET  open = ?,
                high = ?,
                low = ?,
                close = ?,
                volume = ?,
                close_time = ?,
                quote_asset_volume = ?,
                number_of_trades = ?,
                taker_buy_base_asset_volume = ?,
                taker_buy_quote_asset_volume = ?,
                ignore = ?
            WHERE open_time = ?"""
        cursor.execute(
            sql,
            (
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6] / 1000,
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
            ),
            data[0] / 1000,
        )
        conn.commit()
    except:
        conn.rollback()
        raise RuntimeError("Uh oh, an error occurred while updating...")
    # print("----Update Finish----")
    return cursor.lastrowid


def unix_timestamp_to_date():
    create_table()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(open_time) FROM xrp_5_minutes")
    results = cursor.fetchone()
    if results[0] is not None:
        thi = results[0]
        x = thi.split(".")
        print("x")
        print(x)
        ts = int(x[0])
        print("ts - ")
        print(ts)
        # if you encounter a "year is out of range" error the timestamp
        # may be in milliseconds, try `ts /= 1000` in that case
        dateNow = datetime.utcfromtimestamp(ts).strftime("%d %b, %Y")
        print(dateNow)
    else:
        # Upgrade to for weeks prior data from today, for initialization
        dateNow = "15 Jan, 2021"
        print(dateNow)
    return dateNow


def dateTomorrow():
    s = str(datetime.now())
    print(s)
    # '2004/03/30'
    date = datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
    modified_date = date + timedelta(days=1)
    dateTom = datetime.strftime(modified_date, "%d %b, %Y")
    print("dateTomorrow")
    print(dateTom)
    return dateTom


def dedupe_stuff():
    cursor = conn.cursor()
    try:
        cursor.executescript(
            """
            DROP TABLE IF EXISTS xrp_5_minutes_deduped;
            CREATE TABLE xrp_5_minutes_deduped ( 
                            open_time TEXT,
                            open NUMERIC(18,9),
                            high NUMERIC(18,9),
                            low NUMERIC(18,9),
                            close NUMERIC(18,9),
                            volume TEXT,
                            close_time TEXT,
                            quote_asset_volume TEXT,
                            number_of_trades TEXT,
                            taker_buy_base_asset_volume TEXT,
                            taker_buy_quote_asset_volume TEXT,
                            ignore TEXT);
        
            WITH CTE AS(
                SELECT open_time, open, high, low, close, volume, close_time, quote_asset_volume, 
                number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore,
                ROW_NUMBER()OVER(PARTITION BY open_time, open, close_time  ORDER BY open_time) AS rn
                FROM xrp_5_minutes
                ) 
                INSERT INTO  xrp_5_minutes_deduped
                SELECT open_time, open, high, low, close, volume, close_time, quote_asset_volume, 
                number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore
                    FROM CTE
                    WHERE rn = 1
                    ORDER BY 1;
            
            UPDATE xrp_5_minutes_deduped
            SET
                open_time = datetime(open_time, 'unixepoch', 'localtime'),
                close_time = datetime(close_time, 'unixepoch', 'localtime');
            """
        )
        conn.commit()
        # print("1")
    except:
        conn.rollback()
        raise RuntimeError("Uh oh, an error occurred in dedupe_stuff Function...")


def insert_data_key_levels(data):
    cursor = conn.cursor()
    cursor.executescript(
        """
        DROP TABLE IF EXISTS high_key_levels;
        CREATE TABLE high_key_levels(
                number_of_ranges INTEGER NOT NULL,
                price_range_start NUMERIC(6,5) NOT NULL,
                price_range_stop NUMERIC(6,5) NOT NULL,
                high_count INTEGER NOT NULL,
                average_of_start_stop NUMERIC(6,5) NOT NULL);
                        """
    )
    conn.commit()
    for x in data:
        try:
            sql = """
               INSERT INTO high_key_levels (number_of_ranges, price_range_start, price_range_stop, high_count
                                            , average_of_start_stop)
                VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(sql, (x[0], x[1], x[2], x[3], x[4]))
            conn.commit()
        except:
            conn.rollback()
            raise RuntimeError("Uh oh, an error occurred while inserting...")
        # print("----Insert Finished----")
    return cursor.lastrowid


"""
UPDATE
xrp_5_minutes
SET
open_time = datetime(open_time, 'unixepoch', 'localtime'),
close_time = datetime(close_time, 'unixepoch', 'localtime');
"""

# dateTomorrow()
# unix_timestamp_to_date()

dedupe_stuff()
# cursor = conn.cursor()
# create_table()
# ***************************************************************************
# open_time, open, high, low, close, volume, close_time, 0.5469
#'''
def return_xrp_dedupe():
    cursor = conn.cursor()
    # cursor.execute("SELECT COUNT(high) FROM xrp_5_minutes_deduped WHERE high BETWEEN '0.6142599999999999' AND '0.6585199999999999'")
    cursor.execute(
        """
                    SELECT open_time, high, low, open, close
                                FROM xrp_5_minutes_deduped 
                                ORDER BY 1 DESC 
                                LIMIT 70
                    """
    )

    results = cursor.fetchall()
    # print(results)
    # for row in results:
    #   print(row)
    return results


#'''
# ***************************************************************************
'''
# region if tables exists
cursor.execute("""
                 SELECT name FROM sqlite_master WHERE type='table' ;
                 """)
results = cursor.fetchall()
#print(results)
for row in results:
    print(row)
'''
# ***************************************************************************
"""
correctDate = None
try:
    unixts = int("12345672345.0")
    newDate = datetime()
    correctDate = True
except ValueError:
    correctDate = False
print(str(correctDate))
"""
#########################################################################################
'''
cursor = conn.cursor()
cursor.execute("""
               WITH CTE AS(SELECT open_time, high, low, ((high - low)/low)*100 AS avg_len 
                   FROM xrp_5_minutes_deduped 
                   ORDER BY 1 DESC 
                   LIMIT 100
                   )
               SELECT * --MAX(high),  MIN(low), AVG(high), AVG(low), AVG(avg_len)
               , (SELECT close  
                   FROM xrp_5_minutes_deduped
                   ORDER BY open_time DESC
                   LIMIT 1
               ) 
               FROM CTE
               """)

results = cursor.fetchall()
print(results)
'''
