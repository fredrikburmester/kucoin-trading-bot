import json
import time
import base64
import hmac
import hashlib
import requests
import time 
import statistics

from env import API_KEY, API_PASSPHRASE, API_SECRET

## GET DATA ## 

def getOrderBook(symbol):
    # URL
    url = f"{base_url}/api/v1/market/orderbook/level2_20?symbol={symbol}"

    # Time 
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + f"/api/v1/market/orderbook/level2_20?symbol={symbol}"

    # Hash signature
    signature = base64.b64encode(
        hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode(
        'utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())

    # Set request headers
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": API_KEY,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }

    # Response
    try: 
        response = requests.request('get', url, headers=headers)
        res = response.json()
        if res['code'] == '200000':
            return res
        else:
            print("[API Error]", res)
            return {
                'code': '400000'
            }
    except:
        print("[Request Error]")
        return {
            'code': '400000'
        } 

def getStats(symbol):
    # URL
    url = f"{base_url}/api/v1/market/stats?symbol={symbol}"

    # Time 
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + f"/api/v1/market/stats?symbol={symbol}"

    # Hash signature
    signature = base64.b64encode(
        hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode(
        'utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())

    # Set request headers
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": API_KEY,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }

    # Response
    try: 
        response = requests.request('get', url, headers=headers)
        res = response.json()
        if res['code'] == '200000':
            return res
        else:
            print("[API Error]", res)
            return {
                'code': '400000'
            }
    except:
        print("[Request Error]")
        return {
            'code': '400000'
        } 

def getTicker(symbol):
    # URL
    url = f"{base_url}/api/v1/market/orderbook/level1?symbol={symbol}"

    # Time 
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + f"/api/v1/market/orderbook/level1?symbol={symbol}"

    # Hash signature
    signature = base64.b64encode(
        hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode(
        'utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())

    # Set request headers
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": API_KEY,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }

    # Response
    try: 
        response = requests.request('get', url, headers=headers)
        res = response.json()
        if res['code'] == '200000':
            return res
        else:
            print("[API Error]", res)
            return {
                'code': '400000'
            }
    except:
        print("[Request Error]")
        return {
            'code': '400000'
        } 

## ACTIONW ##

def buy():
    pass

def sell():
    pass

def hold():
    pass

# if sell to a loss - reward
# if sell to a gain + reward
# if hold + reward

if __name__ == '__main__':
    base_url = 'https://api.kucoin.com'

    # Define the symbol
    symbol = 'BTC-USDT'

    run = True

    while run:
        stats = getStats(symbol)
        orderBook = getOrderBook(symbol)

        bids = orderBook['data']['bids']
        sell = stats['data']['sell']

        asks = orderBook['data']['asks']
        buy =  stats['data']['buy']

        changeRate =  stats['data']['changeRate']
        changePrice =  stats['data']['changePrice']
        high = stats['data']['high']
        low =  stats['data']['low']
        vol = stats['data']['vol']
        volValue = stats['data']['volValue']
        last = stats['data']['last']
        averagePrice = stats['data']['averagePrice']

        # for index in bids:
        #     index[0] = float(sell) - float(index[0])
        #     print(index[0], index[1])
        
        averageAsk = 0
        for key, value in enumerate(asks):
            value[0] = float(buy) - float(value[0])
                
            if key > 0:
                if value[1] > lastValue[1]:
                    largestAskVolume = value[0]
            lastValue = value

        print(abs(largestAskVolume))

        averageBid = 0
        for key, value in enumerate(bids):
            value[0] = float(sell) - float(value[0])
                
            if key > 0:
                if value[1] > lastValue[1]:
                    largestBidVolume = value[0]
            lastValue = value

        print(largestBidVolume)

        run = False