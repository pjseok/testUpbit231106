import requests
import json

url = "https://api.upbit.com/v1/ticker"

param = {"markets": "KRW-BTC"}

response = requests.get(url, params=param)

result = response.json()

print(result[0]['trade_price']) # 비트코인의 현재가격
print(result[0]['signed_change_rate']) # 부호가 있는 변화율
print(result[0]['acc_trade_price_24h']) # 24시간 누적 거래대금
print(result[0]['acc_trade_volume']) # 24시간 거래량
print(result[0]['high_price']) # 최고가
print(result[0]['low_price']) # 최저가
print(result[0]['prev_closing_price']) # 전일종가
print(result[0]['trade_volume']) # 최근 거래량

