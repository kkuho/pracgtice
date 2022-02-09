import pyupbit
import time
import datetime

global coinlist

tickers = pyupbit.get_tickers(fiat="KRW")
#print(tickers[1:11])
curtime = datetime.datetime.now()
coinlist = []


for item in tickers[1:6] :
    h_itemlists_prev = pyupbit.get_ohlcv(item, interval="minute10", count=10).drop_duplicates()
    h_itemlists = h_itemlists_prev.reset_index().sort_values(by="index", ascending=False) # ticker의 ohlcv 값을 index를 reset해서 내림차순으로 정렬
    #print(h_itemlists)

    if( (h_itemlists.head(1)['index'].item().hour)%24 == curtime.hour) : # 첫번째 기록의 now date기록 중에 시간만 추출해서 지금 시간과 같다면

        coinlist.append([ item, 'null', 0, 0, curtime, h_itemlists.iloc[1]['value'] ]) # 두번째 데이터를 기록하네?? 왜?? 암튼 ticker별로 총거래금액을 기록
        
    #print(coinlist)

    time.sleep(0.1)

sortlist = sorted(coinlist, key=lambda x:x[5], reverse= True)
#print(sortlist)
buyflag = True

for idx, x in enumerate(sortlist) :
    if(buyflag and idx < 10) :
        print(idx, ":", x)
        