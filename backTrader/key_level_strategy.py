from datetime import datetime, timedelta

import backtrader
import pandas as pd

from coinPrice.key_level_finder import conn


class Key_level_strategy(backtrader.Strategy):
    # params = dict(
    #   num_opening_bars=15
    # )
    ################################### GETTING KEY LEVELS ############################
    print("Running Keys Shizzle")
    df2 = pd.read_sql(
        """With Current_price_getter AS (SELECT "close" AS current_price
                FROM xrp_5_minutes_deduped
                ORDER BY open_time DESC 
                LIMIT 1)
           SELECT kl.number_of_ranges, kl.price_range_start, kl.price_range_stop, kl.high_count
                , kl.average_of_start_stop, cpg.current_price
                , ((price_range_stop - price_range_start)/price_range_start)*100 AS percentage_diff_from_current_price
            FROM Current_price_getter cpg, high_key_levels kl
            WHERE --average_of_start_stop < cpg.current_price
                --AND 
                kl.high_count > (SELECT AVG(high_count) FROM high_key_levels) --(average count of high_count from high_key_levels)
                --AND percentage_diff_from_current_price >= 0.2
                ORDER BY  kl.price_range_start DESC , kl.high_count DESC --
                --LIMIT 5
                """,
        conn,
    )
    ##print(df2)
    key_levels = df2.loc[:, "average_of_start_stop"]
    keys = [round(x, 5) for x in key_levels.sort_values()]

    # for x in key_levels.sort_values():
    #    key.append(round(x, 5))
    # print(keys)

    ################################# GETTING KEY LEVELS-ENDS #####################################

    def __init__(self):
        # print("1")
        self.opening_range_low = 0
        self.opening_range_high = 0
        self.opening_range = 0
        # self.bought_today = False
        self.dataclose = self.datas[0].close
        self.order = None
        self.bought_price = None

    def log(self, txt, dt=None):
        # print("2")
        if dt is None:
            dt = self.datas[0].datetime.datetime()

        print("%s, %s" % (dt, txt))

    def notify_order(self, order):
        # print("3")
        if order.status in [order.Submitted, order.Accepted]:
            self.log(
                "ORDER ACCEPTED/SUBMITTED", self.data.num2date(dt=order.created.dt)
            )
            self.order = order
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        if order.status in [order.Completed]:
            order_details = f"{order.executed.price}, Cost: {order.executed.value}, Comm: {order.executed.comm}"

            if order.isbuy():
                self.log(f"BUY EXECUTED, Price: {order_details}")
            elif order.issell():
                self.log(f"SELL EXECUTED, Price: {order_details}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

        """
        next loops through each CandleStick data until the end
        """

    def next(self):
        # range_identification()

        # print("4")
        # print("Candle_price {0}".format(self.dataclose[0]))
        current_bar_datetime = self.data.num2date(self.data.datetime[0])
        previous_bar_datetime = self.data.num2date(self.data.datetime[-1])

        # if 1 != 2:
        self.opening_range_low = self.data.low[0]
        self.opening_range_high = self.data.high[0]
        # self.bought_today = False
        # self.bought_price = None

        # if self.order:
        #     #print('ORDER ALREADY IN')
        #     return

        # global bought_price  # Question is this the best way to store a value during run time?

        if not self.position:
            if self.dataclose[0] < self.keys[0]:
                print(
                    "No trade, Share price too LOW {0} - {1} - {2}".format(
                        self.dataclose[0], current_bar_datetime, self.keys[0]
                    )
                )
                # return
            elif self.dataclose[0] > self.keys[-1]:
                print(
                    "No trade, Share price too HIGH {0} - {1} - {2}".format(
                        self.dataclose[0], current_bar_datetime, self.keys[-1]
                    )
                )
            else:
                # if not self.bought_today:
                newlist = [x for x in self.keys if self.data.close[0] > x]
                print(
                    "close price {0} -- limitBuyPrice {1}".format(
                        self.data.close[0], newlist[-1]
                    )
                )
                self.order = self.buy(
                    exectype=backtrader.Order.Limit,
                    price=newlist[-1],
                    valid=datetime.now() + timedelta(minutes=1),
                )
                self.bought_price = float(
                    newlist[-1]
                )  # setting bought_price value, relates to above question
                # self.order = self.sell(exectype=backtrader.Order.Limit, price=(newlist[-1] + (0.05 * newlist[-1]))
                #                      , valid=datetime.now() + timedelta(minutes=1))
        # '''
        elif self.dataclose[0] >= round(
                (self.bought_price + (0.05 * self.bought_price)), 5
        ):  # 0.01
            # print("Profit selling {0}--{1}".format(
            # self.dataclose[0], round((bought_price + (0.005 * bought_price)), 5)))
            self.order = self.sell()
        elif self.dataclose[0] <= round(
                (self.bought_price - (0.001 * self.bought_price)), 5
        ):
            # print("Loss selling {0}--{1}".format(
            # self.dataclose[0], round((bought_price - (0.001 * bought_price)), 5)))
            self.order = self.sell()
        # '''

    def stop(self):
        # print("5")
        self.log("Ending Value %.2f" % (self.broker.getvalue()))

        if self.broker.getvalue() > 200:
            self.log("*** WINNER ***")

        if self.broker.getvalue() < 200:
            self.log("*** LOSER ***")

# cerebro.plot()
