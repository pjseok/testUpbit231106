import sys
import time
import requests

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

form_class = uic.loadUiType("ui/coinPriceUi.ui")[0]

class CoinViewThread(QThread): # 시그널 클래스
    # 시그널 함수 정의
    coinDateSent = pyqtSignal(float, float, float, float, float, float, float, float)

    def __init__(self):
        super().__init__()
        self.alive = True

    def run(self):
        while self.alive:
            url = "https://api.upbit.com/v1/ticker"

            param = {"markets": "KRW-BTC"}

            response = requests.get(url, params=param)

            result = response.json()

            trade_price = result[0]['trade_price']  # 비트코인의 현재가격
            signed_change_rate = result[0]['signed_change_rate']  # 부호가 있는 변화율
            acc_trade_price_24h = result[0]['acc_trade_price_24h']  # 24시간 누적 거래대금
            acc_trade_volume = result[0]['acc_trade_volume']  # 24시간 거래량
            high_price = result[0]['high_price'] # 최고가
            low_price = result[0]['low_price']  # 최저가
            prev_closing_price = result[0]['prev_closing_price']  # 전일종가
            trade_volume = result[0]['trade_volume']  # 최근 거래량

            # 슬롯에 코인정보 보내주는 함수 호출
            self.coinDateSent.emit(float(trade_price),
                                   float(signed_change_rate),
                                   float(acc_trade_price_24h),
                                   float(acc_trade_volume),
                                   float(high_price),
                                   float(low_price),
                                   float(prev_closing_price),
                                   float(trade_volume))

            time.sleep(1) # api 호출 딜레이(1초마다 한 번씩 업비트 호출)
    def close(self): # close 함수가 호출되면 run 함수(while) 멈춤
        self.alive = False

class MainWindow(QMainWindow, form_class): # 슬롯 클래스

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Coin Price Overview')
        self.setWindowIcon(QIcon('icon/upbiticon.png'))
        self.statusBar().showMessage('ver 1.0')

        self.cvt = CoinViewThread() # 시그널 클래스로 객체 선언
        self.cvt.coinDateSent.connect(self.fillCoinData)
        self.cvt.start() # 시그널 함수의 쓰레드를 시작


    # 시그널클래스에서 보내준 코인정보를 ui에 출력해주는 슬롯함수
    def fillCoinData(self, trade_price, signed_change_rate, acc_trade_price_24h, acc_trade_volume, high_price, low_price,
                     prev_closing_price, trade_volume):
        self.coin_price_label.setText(f"{trade_price:,.0f}원") # 코인의 현재가 출력
        self.coin_changelate_label.setText(f"{signed_change_rate:+.2f}")  # 가격변화율 ->  소수2 자리
        self.acc_trade_price_label.setText(f"{acc_trade_price_24h:,.0f}원")  # 24시간 누적 거래금액
        self.acc_trade_volume_label.setText(f"{acc_trade_volume:.4f}")  # 24시간 거래량
        self.high_price_label.setText(f"{high_price: 0f}원")  # 당일 고가
        self.low_price_label.setText(f"{low_price:,.0f}원")  # 당일 저가
        self.prev_closing_price_label.setText(f"{prev_closing_price:,.0f}원")  # 전일종가
        self.trade_volume_label.setText(f"{trade_volume:.4f}")  # 최근 거래량
        self.updateStyle()

    def updateStyle(self):
        if '-' in self.coin_changelate_label.text():
            self.coin_changelate_label.setStyleSheet("background-color:blue;color:white;")
            self.coin_price_label.setStyleSheet('color:blue;')
        else:
            self.coin_changelate_label.setStyleSheet("background-color:red;color:white;")
            self.coin_price_label.setStyleSheet('color:red;')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())