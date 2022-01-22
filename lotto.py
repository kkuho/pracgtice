    
from random import *

num = range(1,46)
num = list(num)

for i in range(5):
    shuffle(num)
    lotto_num = sample(num, 6)
    print(lotto_num)