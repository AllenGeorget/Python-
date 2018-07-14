class Student(object):
    count = 0

    def __init__(self, name):
        self.name = name
        if len(name) != 0:
            Student.count = Student.count + 1
            #self.count = self.count + 1


# 测试:
if Student.count != 0:
    print('测试失败!')
else:
    bart = Student('Bart')
    print('%d %d' % (Student.count, bart.count))
    if Student.count != 1:
        print('测试失败!')
    else:
        lisa = Student('Bart')
        print('%d %d' % (Student.count, lisa.count))
        if Student.count != 2:
            print('测试失败!')
        else:
            print('Students:', Student.count)
            print('测试通过!')
