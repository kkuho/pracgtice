import pyupbit
import datetime as dt

df = pyupbit.get_ohlcv('KRW-ETH', interval="minute10", count=10).drop_duplicates()
dff = df.reset_index().sort_values(by="index", ascending=False)
dfff = dff.head(1)['index'].item().hour
a = dff.iloc[0]
#print(df)
print(dff)
print(dfff)
print(a)


curtime = dt.datetime.now().hour
print(curtime%24)
#pyupbit.get_ohlcv(item, interval="minute10", count=10).drop_duplicates()