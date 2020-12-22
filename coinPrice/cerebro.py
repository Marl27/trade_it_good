from collection import dedupe_stuff, conn, insert_data_key_levels
from datetime import datetime, timedelta

# conn = db_connect()
candle_data = dedupe_stuff()


def range_identification():
    cursor = conn.cursor()
    cursor.execute("""
                WITH CTE AS(SELECT open_time, high, low FROM xrp_5_minutes_deduped ORDER BY 1 DESC LIMIT 700)
                SELECT MAX(high),  MIN(low)
                FROM CTE
                """)

    results = cursor.fetchall()

    HIGH_RANGE = float(results[0][0])
    LOW_RANGE = float(results[0][1])

    # CALLING grid_maker
    #print(range_splitter(HIGH_RANGE, LOW_RANGE))
    #print()

    #splitted_ranges_in_list_of_tuple(range_splitter(HIGH_RANGE, LOW_RANGE))

    #uncomment these two lines below
    var_getting_key_levels = getting_key_levels(splitted_ranges_in_list_of_tuple(range_splitter(HIGH_RANGE, LOW_RANGE)))
    insert_data_key_levels(var_getting_key_levels)


'''
range_splitter(HIGH_RANGE, LOW_RANGE)
defining 50 intervarls between high and low price
'''
def range_splitter(h, l):
    i = l
    # global range_splitter_list
    range_splitter_list = []
    # num calculates how many dividers we want in the high_lowgrid
    num = (h - l) / 50
    print("Intervals: " + str(20))
    print("Number to add in highs: " + str(num))
    while i <= h:
        i += num
        range_splitter_list.append(i)
    #print("i: " + str(i))
    if i > l:
        range_splitter_list.remove(i)
        # print(i)
    # print(range_splitter_list)
    # splitted_ranges_in_list_of_tuple(range_splitter_list)
    return range_splitter_list


'''
def splitted_ranges_in_list_of_tuple(rsl):
adds range_splitter_list in a list of tuples. So that it could be easily used in a query
'''
def splitted_ranges_in_list_of_tuple(rsl):
    #global splitted_ranges_list_of_tuple
    splitted_ranges_list_of_tuple = []
    i = 0
    # for i in range(len(range_splitter_list)):
    while i < len(rsl) - 1:
        # if i == len(range_splitter_list)-1:
        #   break
        splitted_ranges_list_of_tuple.append((i, rsl[i], rsl[i + 1]))
        #print("inside LOOP: " + str(splitted_ranges_list_of_tuple))
        i += 1
    #print("outside LOOP: " + str(splitted_ranges_list_of_tuple))
    return splitted_ranges_list_of_tuple


# '''
def getting_key_levels(srlt):
    cursor = conn.cursor()
    key_levels_list = []
    for x in range(len(srlt)):
        var = srlt[x]
        #print(var)
        cursor.execute("SELECT COUNT(high) FROM xrp_5_minutes_deduped WHERE high BETWEEN ? AND ?", (var[1], var[2]))
        high = cursor.fetchone()
        cursor.execute("SELECT COUNT(high) FROM xrp_5_minutes_deduped WHERE low BETWEEN ? AND ?", (var[1], var[2]))
        low = cursor.fetchone()
        key_level = high[0] + low[0]
        average = (float(var[1]) + float(var[2])) / 2
        # print(average)
        #print(results)
        #print(str(var[0]) + " : " + str(var[1]) + " : " + str(var[2]) + " : " + str(results[0]) + " : " + str(average))
        key_levels_list.append((var[0], var[1], var[2], key_level, average))

    return key_levels_list

    # for row in results:
range_identification()
#print("Global Range Splitter List: " + str(splitted_ranges_list_of_tuple))

'''
cursor = conn.cursor()
key_levels_list = []
for x in range(len(splitted_ranges_list_of_tuple)):
    var = splitted_ranges_list_of_tuple[x]
    print(var)
    cursor.execute("SELECT COUNT(high) FROM xrp_5_minutes_deduped WHERE high BETWEEN ? AND ?", (var[1], var[2]))
    high = cursor.fetchone()
    cursor.execute("SELECT COUNT(high) FROM xrp_5_minutes_deduped WHERE low BETWEEN ? AND ?", (var[1], var[2]))
    low = cursor.fetchone()
    key_level = high[0] + low[0]
    average = (float(var[1]) + float(var[2])) / 2
    # print(average)
    print(str(high[0]) + " : " + str(low[0]))
    print(str(var[0]) + " : " + str(var[1]) + " : " + str(var[2]) + " : " + str(high[0]) + " : " + str(low[0]) + " : "
          + str(average))
    key_levels_list.append((var[0], var[1], var[2], key_level, average))
'''




'''
cursor = conn.cursor()
cursor.execute("""SELECT * --MIN(average_of_start_stop) 
                    FROM high_key_levels
                    WHERE average_of_start_stop > '0.5530'
                    AND high_count < 9
                    AND high_count > 0
                    ORDER BY high_count DESC, price_range_start
                    --LIMIT 1
                """)
results = cursor.fetchall()
for x in results:
    print(x)
'''