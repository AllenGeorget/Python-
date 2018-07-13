# -*- coding: utf-8 -*-
from functools import reduce
DIGITS={'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def char2num(sss):
    return DIGITS[sss]
def fun(x,y):
    return x*10+y
def count(s):
    i=0
    while s[i]!='.':
        i=i+1
    return len(s)-i-1
def str2float(s):
    s1 = s.replace('.','')
    ss=reduce(fun,map(char2num,s1))
    i=0
    j=count(s)
    num=1
    while i<j: 
        num=num*10
        i=i+1
    ss=ss/num
    return ss


print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('测试成功!')
else:
    print('测试失败!')