from collection import dedupe_stuff, conn, insert_data_key_levels

# conn = db_connect()

candle_data = dedupe_stuff()
"""subtract the old price from the new price and divide the difference by the old price. 
    Then, multiply by 100 to get the percent change"""


def range_identification():
    cursor = conn.cursor()
    cursor.execute(
        """
                WITH CTE AS(SELECT open_time, high, low, ((high - low)/low)*100 AS avg_len 
                    FROM xrp_5_minutes_deduped 
                    ORDER BY 1 DESC 
                    LIMIT 500
                    )
                SELECT MAX(high),  MIN(low), AVG(high), AVG(low), AVG(avg_len)
                , (SELECT close  
                    FROM xrp_5_minutes_deduped
                    ORDER BY open_time DESC
                    LIMIT 1
                ) 
                FROM CTE
                """
    )

    results = cursor.fetchall()
    # print(results)
    HIGH_RANGE = float(results[0][0])
    LOW_RANGE = float(results[0][1])
    AVG_HIGH = float(results[0][2])
    AVG_LOW = float(results[0][3])
    global AVG_LENGTH
    AVG_LENGTH = float(results[0][4])
    print("AVG_LENGTH: " + str(AVG_LENGTH))

    global avg_difference
    avg_difference = AVG_HIGH - AVG_LOW
    print("avg_difference: " + str(avg_difference))

    global CURRENT_PRICE
    CURRENT_PRICE = str(results[0][5])
    print("CURRENT_PRICE: " + str(CURRENT_PRICE))

    # for row in results:
    #    print(row)
    # CALLING grid_maker
    # print(range_splitter(HIGH_RANGE, LOW_RANGE))
    # print()

    # splitted_ranges_in_list_of_tuple(range_splitter(HIGH_RANGE, LOW_RANGE))

    # uncomment these two lines below
    var_getting_key_levels = getting_key_levels(
        splitted_ranges_in_list_of_tuple(range_splitter(HIGH_RANGE, LOW_RANGE))
    )
    # print("getting KEy LEvels: " + str(var_getting_key_levels))
    insert_data_key_levels(var_getting_key_levels)


def range_splitter(h, l):
    """
    range_splitter(HIGH_RANGE, LOW_RANGE)
    defining 50 intervarls between high and low price
    >>> range_splitter(10, 5)
    []
    """
    i = l
    # global range_splitter_list
    range_splitter_list = []
    # num calculates how many dividers we want in the high_lowgrid
    intervals = 200
    num = (h - l) / intervals  # list(range(10, 30, 2))
    print("Intervals: " + " " + str(intervals))
    print("Number to add in highs: " + str(num))
    while i <= h:
        i += num
        range_splitter_list.append(i)
    # print("i: " + str(i))
    if i > l:
        range_splitter_list.remove(i)
        # print(i)
    # print(range_splitter_list)
    # splitted_ranges_in_list_of_tuple(range_splitter_list)
    return range_splitter_list


"""
def splitted_ranges_in_list_of_tuple(rsl):
adds range_splitter_list in a list of tuples. So that it could be easily used in a query
"""


def splitted_ranges_in_list_of_tuple(rsl):
    # global splitted_ranges_list_of_tuple
    splitted_ranges_list_of_tuple = []
    i = 0
    # for i in range(len(range_splitter_list)):
    while i < len(rsl) - 1:
        # if i == len(range_splitter_list)-1:
        #   break
        splitted_ranges_list_of_tuple.append((i, rsl[i], rsl[i + 1]))
        # print("inside LOOP: " + str(splitted_ranges_list_of_tuple))
        i += 1
    # print("outside LOOP: " + str(splitted_ranges_list_of_tuple))
    # print(splitted_ranges_list_of_tuple)
    return splitted_ranges_list_of_tuple


# '''
def getting_key_levels(srlt):
    cursor = conn.cursor()
    key_levels_list = []
    for x in range(len(srlt)):
        var = srlt[x]
        # print(var)
        cursor.execute(
            "SELECT COUNT(high) FROM xrp_5_minutes_deduped WHERE high BETWEEN ? AND ?",
            (var[1], var[2]),
        )
        high = cursor.fetchone()
        cursor.execute(
            "SELECT COUNT(low) FROM xrp_5_minutes_deduped WHERE low BETWEEN ? AND ?",
            (var[1], var[2]),
        )
        low = cursor.fetchone()
        # print("high: " + str(high[0]))
        # print("low: " + str(low[0]))
        key_level = high[0] + low[0]
        average = (float(var[1]) + float(var[2])) / 2
        """average = Average price of the candle to make 'KEY_LEVEL'/SUPPORT/RESISTANCE"""
        # print(average)
        # print(str(var[0]) + " : " + str(var[1]) + " : " + str(var[2]) + " : " + str(results[0]) + " : " + str(average))
        key_levels_list.append((var[0], var[1], var[2], key_level, average))
        # key_levels_list.append((var[0], var[1], var[2], low[0], average))
    return key_levels_list


"""
def adding_numbers(a, b):
    return a+b
"""
range_identification()
print("************************************************************")

# for row in results:
# print("Global Range Splitter List: " + str(splitted_ranges_list_of_tuple))

"""is_trade_profitable"""
# broker fee - 0.1000% of the trade

'''

cursor = conn.cursor()
sql = """
        With Current_price_getter AS (SELECT "close" AS current_price
                    FROM xrp_5_minutes_deduped
                    ORDER BY open_time DESC 
                    LIMIT 1)
               SELECT kl.number_of_ranges, kl.price_range_start, kl.price_range_stop, kl.high_count
                    , kl.average_of_start_stop, cpg.current_price
                    --, ((price_range_stop - price_range_start)/price_range_start)*100 AS percentage_diff_from_current_price
                FROM Current_price_getter cpg, high_key_levels kl
                WHERE average_of_start_stop < cpg.current_price
                    AND kl.high_count > (SELECT AVG(high_count) FROM high_key_levels)  --(average count of high_count from high_key_levels)
                    ORDER BY  kl.price_range_start DESC , kl.high_count DESC --
                    LIMIT 5
        """
cursor.execute(sql)
results = cursor.fetchall()
keys = [(x[4],x[5]) for x in results]
#for x in results:
print("ROWs: " + str(keys))
'''


'''
cursor = conn.cursor()

sql = """SELECT *  , ((average_of_start_stop - ?)/?)*100 AS percentage_diff_from_current_price
            FROM high_key_levels
            WHERE average_of_start_stop >= ? 
            AND high_count <= 9
            AND high_count > 0
            AND percentage_diff_from_current_price >= 0.5
            ORDER BY high_count DESC, price_range_start
            --LIMIT 8
        """
cursor.execute(sql, (CURRENT_PRICE, CURRENT_PRICE, CURRENT_PRICE))
results = cursor.fetchall()
for x in results:
    print("ROWs: " + str(x))
'''
