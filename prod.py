from functools import reduce
def prod(L):
    return reduce(fun,L)
def fun(x1,x2):
    return x1*x2
print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')