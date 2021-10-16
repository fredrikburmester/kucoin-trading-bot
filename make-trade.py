import json
import time
import base64
import hmac
import hashlib
import requests
import time 
import statistics
import sys

from env import API_KEY, API_PASSPHRASE, API_SECRET

############### BUY #################
def buy(symbol, funds):
    print(time.time())

    data={
        'symbol': symbol,
        'type': 'market',
        'funds': funds,
        'side': 'buy',
        'clientOid': f"{str(time.time())}",
    }
    data_json = json.dumps(data)

    # URL
    url = f"{base_url}/api/v1/orders"

    # Time 
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'POST' + f"/api/v1/orders{data_json}"

    # Hash signature
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())

    # Set request headers
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        "Content-Type": "application/json"
    }

    # Response
    try:
        response = requests.request('POST', url, headers=headers, data=data_json)
        # print(response.json())
        res = response.json()
        if res['code'] == '200000':
            print(f"\n✅ Successfully bought ${funds} of {symbol} | ID: {res['data']['orderId']}")
            return res['data']['orderId']
        else:
            print(response.json())
    except NameError: 
        print("Error: ", NameError)

############### GET ORDER BY ID #################
def getOrderById(id):
    # Get recent order 
    url = f"{base_url}/api/v1/orders/{id}"

    # Time 
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + f"/api/v1/orders/{id}"

    # Hash signature
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())

    # Set request headers
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }

    # Response
    try:
        response = requests.request('get', url, headers=headers)
        res = response.json()
        if res['code'] == '200000':
            dealSize = res['data']['dealSize']
            dealFunds = res['data']['dealFunds']
            symbol = res['data']['symbol']
            print(f"\nSuccessfully got latest order: 📈")
            print(f"Buy: ${float(dealFunds)/float(dealSize)}")
            print(f"Amount: {dealSize} of {symbol}\n")
            return [dealSize, dealFunds, symbol]
        else:
            print(response.json())
    except NameError: 
        print("Error: ", NameError)

############### SELL #################
def sell(id, dealFunds, dealSize, precision, multiplier):
    # Place the sell order
    price = (float(dealFunds) / float(dealSize)) * float(multiplier)
    price = round(price, int(precision))
    size = float(dealSize) * 0.999
    size = round(size, 2)


    data={
        'symbol': symbol,
        'price': price,
        'size': str(size),
        'type': 'limit',
        'side': 'sell',
        'clientOid': '1234fdafdsas',
    }
    data_json = json.dumps(data)

    # URL
    url = f"{base_url}/api/v1/orders"

    # Time 
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'POST' + f"/api/v1/orders{data_json}"

    # Hash signature
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())

    # Set request headers
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        "Content-Type": "application/json"
    }

    # Response
    try:
        response = requests.request('POST', url, headers=headers, data=data_json)
        res = response.json()
        if res['code'] == '200000':
            print(f"✅ Successfully placed limit sell with {multiplier}X price!")
        else:
            print(response.json())
    except NameError: 
        print("Error: ", NameError)


############### GET PRECISION #################
def getTickerInformation(symbol):
    # Get recent order 
    url = f"{base_url}/api/v1/symbols/{symbol}"

    # Time 
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + f"/api/v1/symbols/{symbol}"

    # Hash signature
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())

    # Set request headers
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }

    # Response
    try:
        response = requests.request('get', url, headers=headers)
        res = response.json()
        if res['code'] == '200000':
            return res['data']['priceIncrement']
        else:
            print(response.json())
    except NameError: 
        print("Error: ", NameError)

############### MAIN #################
if __name__ == '__main__':
    base_url = 'https://api.kucoin.com'
    api_key = API_KEY
    api_secret = API_SECRET
    api_passphrase = API_PASSPHRASE
    
    # Get command line arguments
    if len(sys.argv) != 4:
        print("Wrong arguments")
        exit()
    
    symbol = sys.argv[1] + "-USDT"
    funds = sys.argv[2]
    multiplier = sys.argv[3]
    print(f"\nℹ️ Trying to buy {symbol} for ${funds} with a limit sell for {multiplier}X gains!")

    try:
       # Buy and get order id back
        id = buy(symbol, funds)

        # Pause for the order to go through
        # time.sleep(1)

         # Get last order from id
        # id = "60b72b87fde2670006c4b89f"
        [dealSize, dealFunds, symbol] = getOrderById(id)
        precision = getTickerInformation(symbol)
        precision = len(precision) - 2

        # Try to sell the last order 
        sell(id, dealFunds, dealSize, precision, multiplier)
    except NameError: 
        print("Error: ", NameError)
        print("Something went wrong 😰 ")
