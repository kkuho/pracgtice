import pyupbit
import time
import datetime
from openpyxl import load_workbook

with open("djqqlxm.txt") as f: # upbit login
    lines = f.readlines()
    key = lines[0].strip() #strip 공백 제거
    secret = lines[1].strip()
    upbit = pyupbit.Upbit(key, secret)

balance = upbit.get_balances()
balance_krw = upbit.get_balance()

#print(balance)
print(balance_krw * 0.05)
