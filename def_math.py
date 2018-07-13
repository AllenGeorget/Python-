import math
def quadratic(a,b,c):
    d=b*b-4*a*c
    if d < 0:
        return '方程无解'
    else:
        x1 = (-b + math.sqrt(d))/(2*a)
        x2 = (-b - math.sqrt(d))/(2*a)
        return x1,x2

print(quadratic(1,2,1))