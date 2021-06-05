import random
n = 100
w = 100000

a = []
b= []

for i in range(n):
    a.append(random.randint(101,301))

for i in range(n):
    b.append(random.randint(1,10))

print(n,w)
print(*a)
print(*b)
