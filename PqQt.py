import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import pyupbit
import time
import datetime



with open("djqqlxm.txt") as f: # upbit login
    lines = f.readlines()
    key = lines[0].strip() #strip 공백 제거
    secret = lines[1].strip()
    upbit = pyupbit.Upbit(key, secret)


def get_target_price(ticker): # 변동성 돌파 구간 계산 

    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    
    return target

def get_yesterday_ma5(ticker): # 5일 평균선 
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]

ticker_input = input("원하는 Ticker를 입력하시오 : ")
ma5 = get_yesterday_ma5(ticker_input)
target_price = get_target_price(ticker_input)
balance = round(upbit.get_balance())



form_class = uic.loadUiType("upbitCurrentPrice.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.inquiry)

        
    def inquiry(self):
        cur_time = QTime.currentTime() #  현재 시간을 받아오고
        str_time = cur_time.toString("hh:mm:ss") #  현재 시간을 문자열로 변경
        self.statusBar().showMessage(str_time) # 시간을 window 창에 출력하는 함수
        
        price = pyupbit.get_current_price(ticker_input)
        if (price > target_price) and (price > ma5):
            sayho = "가즈아아아아!!!"
            
        else:
            sayho = "기다려!!!"


        self.lineEdit.setText(str(format(price, ','))) # lineEdit 에 price 문자열 값 출력
        self.lineEdit_2.setText(str(format(target_price, ',')))
        self.lineEdit_3.setText(str(format(ma5, ',')))
        self.lineEdit_4.setText(ticker_input)
        self.lineEdit_5.setText(str(format(balance, ',')))
        self.lineEdit_6.setText(sayho)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()