def trim(s):
    if s=='':
        return s
    i=0
    j=len(s)-1
    while s[int(i)]==' ':
        i=i+1
        if i==j:
            return ''
    while s[int(j)]==' ':
        j=j-1
    j=j+1
    print(s[int(i):int(j)])
    return s[int(i):int(j)]
# 测试:
if trim('hello  ') != 'hello':
    print('1测试失败!')
elif trim('  hello') != 'hello':
    print('2测试失败!')
elif trim('  hello  ') != 'hello':
    print('3测试失败!')
elif trim('  hello  world  ') != 'hello  world':
    print('4测试失败!')
elif trim('') != '':
    print('5测试失败!')
elif trim('    ') != '':
    print('6测试失败!')
else:
    print('7测试成功!')