import json
import time
import base64
import hmac
import hashlib
import requests
import time 
import statistics

from env import API_KEY, API_SECRET, API_PASSPHRASE

base_url = 'https://api.kucoin.com'
api_key = API_KEY
api_secret = API_SECRET
api_passphrase = API_PASSPHRASE

long = False
lastBuyPrice = 0
totalProfit = 0

# Define the symbol
symbol = 'BTC-USDT'

def getTicker(symbol):
    # URL
    url = f"{base_url}/api/v1/market/orderbook/level1?symbol={symbol}"

    # Time 
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + f"/api/v1/market/orderbook/level1?symbol={symbol}"

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
            return res
        else:
            print("Something went wrong 😰 ")
            print(res)
            return {
                'code': '400000'
            }
    except:
        print("[API Error] Something went wrong 😰 ")
        return {
            'code': '400000'
        } 

def calculateRSI(averageGain, averageLoss):
    if averageLoss == 0:
        return 100

    if averageGain == 0:
        return 0

    RS = averageGain / averageLoss
    return 100 - (100/(1+(RS)))

def evaluateTrade(RSI, price, lastRSI):
    global long
    global lastBuyPrice
    global totalProfit

    if long == True and lastRSI > 70 and RSI < lastRSI:
        sell(price)
    elif long == False and RSI < 25 and RSI > lastRSI:
        print("\n🟢 BUY @", price)
        lastBuyPrice = price
        long = True

    # Stop loss
    if long == True and (price/lastBuyPrice) < 0.998:
        print(f"❌ Stop loss activated! @{price}")
        sell(price)

    # Limit sell
    if long == True and (price/lastBuyPrice) > 1.004:
        sell(price)

def evaluateVolumeTrade(price):
    global long
    global lastBuyPrice
    global totalProfit

    # Stop loss
    if long == True and (price/lastBuyPrice) < 0.995:
        print(f"❌ Stop loss activated! @{price}")
        sell(price)

    # Limit sell
    if long == True and (price/lastBuyPrice) > 1.01:
        sell(price)

def sell(price):
    global lastBuyPrice
    global totalProfit
    global long

    print("\nSELL @", price)
    totalProfit += (price - lastBuyPrice)/price
    print(f"Total profit: {round(totalProfit, 4)}%")
    long = False

def buy(price):
    global lastBuyPrice
    global long

    if not long:
        print("\n🟢 BUY @", price)
        lastBuyPrice = price
        long = True

def calculateRS():
    # List of last 14 gain/loss calculations
    gains = []
    losses = []

    # Calculate first medians of 14 datapoints
    previousPrice = 0
    print("\nCalculating RS... ")
    for i in range(n + 1): 
        print(str(int((100/(n + 1))*(i+1))) + "%" )
        gain = 0
        loss = 0

        ticker = getTicker(symbol)

        if ticker['code'] == '200000':
            price = float(ticker['data']['price'])

            # Base case
            if i == 0:
                previousPrice = price
            
            # Calculate Gain/Loss
            if i > 0:
                if price >= previousPrice:
                    gain = abs(price - previousPrice)
                    gains.append(gain)
                else: 
                    loss = abs(price - previousPrice)
                    losses.append(loss)
        sleep()

    # Here are the average gains/losses
    averageGain = sum(gains) / n
    averageLoss = sum(losses) / n
            
    print("Done!\n")
    return averageGain, averageLoss

def sleep():
    seconds = 10
    time.sleep(seconds)

if __name__ == '__main__':
    # Datapoints for RSI
    n = 6

    # Main loop
    i = 0
    previousPrice = 0

    averageGain, averageLoss = calculateRS()

    while True: 
        gain = 0
        loss = 0

        ticker = getTicker(symbol)
        if ticker['code'] == '200000' and ticker['data'] != None:
            price = float(ticker['data']['price'])


            # # First time
            if i == 0:
                previousPrice = price

            # print(ticker['data'])

            priceDiff = price - previousPrice
            kValue = priceDiff / price 
            if kValue < -0.0001: # if volatility higher than 5%
                print("High volatility alert!")
                print(priceDiff)

                if not long:
                    buy(price)
                elif long:
                    sell(price)

            evaluateVolumeTrade(price)

            
            # Calculate Gain or Loss
            if price > previousPrice:
                gain = abs(price - previousPrice)
                #print(f"🟢 {price} {str(round(((price - previousPrice)/price) * 100, 2))}%")
            elif price < previousPrice: 
                loss = abs(price - previousPrice)
                #print(f"🔴 {price} {str((round((price - previousPrice)/price) * 100, 2))}%" )
            
            # Calculate new RS 
            averageGain = ((averageGain * (n-1)) + gain) / n
            averageLoss = ((averageLoss * (n-1)) + loss) / n

            # Calculate RSI
            RSI = calculateRSI(averageGain, averageLoss)

            # Evaluate the trade
            # if i > n:
            #     evaluateTrade(RSI, previousPrice, lastRSI)

            # Print updates
            print("\nRSI:", RSI)
            print("📈 ", round(kValue, 4))

            lastRSI = RSI

            # if totalProfit != 0:
            #     print(f"Total profit: {round(totalProfit, 4)}% with a 10x margin = {round(totalProfit, 4) * 10} ")

            # Set last price and RSI
            previousPrice = price

            i += 1
        else: 
            print(ticker)
        sleep()

        
    