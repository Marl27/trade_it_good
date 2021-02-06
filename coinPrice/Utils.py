from __future__ import annotations
from typing import Tuple


class Candle:
    def __init__(self, date:str, high:float, low:float, close:float, open_price:float):
        self.date = date
        self.high = high
        self.low = low
        self.close = close
        self.open_price = open_price

    def __repr__(self) -> str: #
        return f"{self.date}, {self.high}, 2"

    def size(self) -> float:
        return self.high - self.low

    def size_of_the_candle(self) -> Tuple[float, float, float]:
        """
        size_of_the_candle(20, 1)
        >>> my_candle = Candle("data", 20, 1, 19, 5)
        >>> my_candle.size_of_the_candle()
        (20, 1, 1900.0)
        """
        # print(my_candle.size_of_the_candle.__doc__)
        return (self.high, self.low, ((self.high - self.low) / self.low) * 100)

    # open_time, high, low, ((high - low) / low) * 100
    # AS
    # avg_len

    def average_price(self) -> float:
        """
        >>> my_candle = Candle("data", 20, 1, 19, 5)
        >>> my_candle.average_price()
        10.5
        :return:
        """
        return (self.low + self.high) / 2

    def __mul__(self, n) -> Candle:
        return Candle(self.date, self.high * n,self.low * n,self.open_price * n, self.close * n)

my_candle = Candle("data", 20, 1, 19, 5)

##write a helper function
## use magic method in the Candle
## Serialize to disk, tojson 

# print(my_candle.size_of_the_candle()) #prints 'Foo'

# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
