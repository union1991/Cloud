# 공백없이 주어진 숫자의 합 구하기

n = int(input())
t = input()
list1=[]

for i in range(0,n):
    k = t[i:i+1]
    list1.append(int(k))

print(sum(list1))
