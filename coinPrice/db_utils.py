import os
import sqlite3
import random
from sqlalchemy import create_engine


# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def db_connect(db_path=DEFAULT_PATH):
    engine = create_engine(f'sqlite:///{db_path}')
    con = sqlite3.connect(db_path)
    print(random.randint(1, 9))
    return con

db_path = os.path.join(os.path.dirname(__file__), "my_new_database.db")
engine = create_engine(f'sqlite:///{db_path}')
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String
class xrp_5_minutes(Base):

    def __repr__(self):
        return f"candle: data= {self.open_time}, high = {self.high}"

    __tablename__ = 'xrp_5_minutes'
    open_time = Column(String, primary_key=True)
    open = Column(String)
    high = Column(String)
    low = Column(String)
    close = Column(String)
    volume = Column(String)
    close_time = Column(String)
    quote_asset_volume = Column(String)
    number_of_trades = Column(String)
    taker_buy_base_asset_volume = Column(String)
    taker_buy_quote_asset_volume = Column(String)
    ignore = Column(String)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

session = Session()

for i in range(10):
    a = xrp_5_minutes(open_time=f'open_{i}', open='open', high= 'high_price', low='low_price', close='close_price',
                  volume='volume', close_time='close_t', quote_asset_volume='quote_asset_volume',
                  number_of_trades='number_of_trades', taker_buy_base_asset_volume='taker_buy_base_asset_volume',
                  taker_buy_quote_asset_volume='taker_buy_quote_asset_volume', ignore='ignore')
    session.add(a)





Base.metadata.create_all(engine)


# def db_connect(db_path=DEFAULT_PATH):
#     con = sqlite3.connect(db_path)
#     print(random.randint(1, 9))
#     return con

# db_connect()
