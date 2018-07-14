def createCounter():
    def count():
        n=1
        while True:
            yield n
            n=n+1
    x=count()
    def counter():
        return next(x)
    return counter
    
    # def counter():
    #     x=count()
    #     return next(x)
    # return counter错误

# 测试:
counterA = createCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA()) # 1 2 3 4 5
counterB = createCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')