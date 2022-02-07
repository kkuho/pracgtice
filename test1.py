import pyupbit
import time
import datetime
from openpyxl import load_workbook

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

def write_target(ticker_input, target_price, ma5): # trade 정보를 엑셀로 기록하는 함수
    
    wb = load_workbook('upbitRecord.xlsx')
    ws = wb[wb.sheetnames[1]]
    row = []

    row.append(ticker_input)
    row.append(target_price)
    row.append(ma5)

    ws.append(row)
    wb.save('upbitRecord.xlsx')


ticker_input = input("원하는 ticker를 입력하세요 : ")
ma5 = get_yesterday_ma5(ticker_input)
target_price = get_target_price(ticker_input)
write_target(ticker_input, target_price, ma5)