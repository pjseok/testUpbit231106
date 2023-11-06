import requests
import pyupbit

url = "https://api.upbit.com/v1/market/all?isDetails=false"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)

tickerlist = pyupbit.get_tickers(fiat='KRW')
print(tickerlist)

coinTickerList = []

for ticker in tickerlist:
    # print(ticker[4:])
    coinTickerList.append(ticker[4:])

print(coinTickerList)