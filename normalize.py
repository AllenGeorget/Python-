def normalize(name):
    name2=name[0].upper()+name[1:].lower()
    return name2
#测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)