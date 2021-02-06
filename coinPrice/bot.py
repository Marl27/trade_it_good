import sys
sys.path.insert(0,'C:/Users/himal/Desktop/trading_bot')
import websocket, json, pprint
# websocket-client
# python-binance
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/xrpusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.05

closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET) #, tld='us')


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True


def on_open(ws):
    print('opened connection')
    print(config.API_KEY)


def on_close(ws):
    print('closed connection')


def on_message(ws, message):
    print('received message')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']



ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()