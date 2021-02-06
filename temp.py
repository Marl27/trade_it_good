from typing import List


def range_splitter(h:int, l:int)->List[int]:
    """
    range_splitter(HIGH_RANGE, LOW_RANGE)
    defining 50 intervarls between high and low price
    >>> range_splitter(50, 10)
    [10, 14, 18, 22, 26, 30, 34, 38, 42, 46]
    >>> range_splitter(10, 60)
    [60, 55, 50, 45, 40, 35, 30, 25, 20, 15]

    """
    i = l
    # global range_splitter_list
    range_splitter_list = []
    # num calculates how many dividers we want in the high_lowgrid
    num = (h - l) / 10  # list(range(10, 30, 2))
    return list(range(l, h, int(num)))
    # print("Intervals: " + str(50))
    # print("Number to add in highs: " + str(num))
    # while i <= h:
    #     i += num
    #     range_splitter_list.append(i)
    # #print("i: " + str(i))
    # if i > l:
    #     range_splitter_list.remove(i)
    #     # print(i)
    # # print(range_splitter_list)
    # # splitted_ranges_in_list_of_tuple(range_splitter_list)
    # return range_splitter_list

range_splitter(12.3, 5.98776)
