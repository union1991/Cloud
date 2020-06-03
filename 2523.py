# 별 찍기-13

a = int(input())
n = 2*a

for i in range(1, n) :
    if a >= i :
        print('*'*i)
    else :
        print('*'*((2*a)-i))
