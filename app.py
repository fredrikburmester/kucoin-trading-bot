import json
import time
import base64
import hmac
import hashlib
import requests

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

from env import API_KEY, API_PASSPHRASE, API_SECRET

base_url = 'https://api.kucoin.com'
api_key = API_KEY
api_secret = API_SECRET
api_passphrase = API_PASSPHRASE

def getTickerPrice(ticker):
    url = f"{base_url}/api/v1/market/orderbook/level1?symbol={ticker}"

    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + f"/api/v1/market/orderbook/level1?symbol={ticker}"

    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = requests.request('get', url, headers=headers)
    return response.json()

def getHistoricalOrders():
    url = f"{base_url}/api/v1/fills?currentPage=1&pageSize=100"

    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + \
        f"/api/v1/fills?currentPage=1&pageSize=100"

    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = requests.request('get', url, headers=headers)
    return response.json()

def getPersonalHoldings():
    url = 'https://api.kucoin.com/api/v1/accounts'
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode(
        'utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    response = requests.request('get', url, headers=headers)
    return response



@app.route('/')
def hello_world():
    # return response.json()
    return render_template('index.html', name="Home")


@app.route('/api/data', methods=['GET'])
def getData():
    data = getPersonalHoldings()
    data = data.json()
    data = data['data']

    labels = []
    balance = []

    for i in data:
        if float(i['balance']) > 0:
            labels.append(i['currency'])
            balance.append(i['balance'])

    result = {
        "labels": labels,
        "balance": balance
    }
    print(result)
    return result; 

@app.route('/api/ticker/<ticker>')
def tickerPrice(ticker):
    return getTickerPrice(f'{ticker}-USDT')


@app.route('/api/hist-orders')
def historicalOrders():
    return getHistoricalOrders()

if __name__ == '__main__':
    app.run(debug=True)

