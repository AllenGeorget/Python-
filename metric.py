# Not fully understood
# 廖雪峰-Python教程-函数式编程-装饰器
# -*- coding:utf-8 -*-
import time
import functools


def metric(fn):
    @functools.wraps(fn)
    def wrapper(*arg, **kw):
        before = time.time()
        func = fn(*arg, **kw)
        end = time.time()
        t = (end - before) * 1000
        print("执行%s耗时：%f ms" % (fn.__name__, t))
        return func##return fn is wrong
    return wrapper

# 测试
@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y;

@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z;

f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')