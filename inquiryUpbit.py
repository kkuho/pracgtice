from xml.dom.minidom import parseString
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

def buy_crypto_currency(ticker): # 매수
    krw = upbit.get_balance() # 예수금 확인
    orderbook = pyupbit.get_orderbook(ticker)

    asks = orderbook['orderbook_units']
    sell_price = asks[0]['ask_price']
    unit = krw / float(sell_price) # float 은 실수형으로 만들어주는 함수
    upbit.buy_market_order(ticker, unit) # 현재 시장가로 구매 가능한 수량을 구매 ! 주의!! 실행하는 순간 매수됨
    

def sell_crypto_currency(ticker): # 매도 
    unit_sell = upbit.get_balance(ticker)
    upbit.sell_market_order(ticker, unit_sell)


def get_yesterday_ma5(ticker): # 5일 평균선 
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]


now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1) # 자정 시간을 구하는 함수 식
ticker_input = input("원하는 ticker를 입력하세요 : ")
ma5 = get_yesterday_ma5(ticker_input)
target_price = get_target_price(ticker_input) # 이 코드 실행할 때 target 가격을 계산

while True:
    try:
        now = datetime.datetime.now()
        current_price = pyupbit.get_current_price(ticker_input)
        if mid < now < mid + datetime.timedelta(seconds=10): # 정각에서 10초 내에 있을 때 자정으로 간주함
            print("정각입니다!!")
            target_price = get_target_price(ticker_input)
            ma5 = get_yesterday_ma5(ticker_input)
            now = datetime.datetime.now()
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            #sell_crypto_currency(ticker_input)
        
        if (current_price > target_price) and (current_price > ma5):
            pass
  
            #buy_crypto_currency(ticker_input)
        else:
            print(now, "|", "현재가 : " , current_price, "|", "목표가 : ", target_price, "|",  "5일선 평균가 : ", ma5)
        

    except:
        print("에러 발생")
        
    time.sleep(1)
    
        






