# without repetitions
# import random
# values = random.sample(range(1, 4000), 1000)
# for i in values:
#     print(i, ', ', sep='', end='')


# with repetitions
from numpy.random import seed
from numpy.random import randint
seed(1)
values = list(randint(0, 1000, 1000))
d={}
for i in values:
    # print(i, ', ', sep='', end='')
    if i in d:
        d[i]+=1
    else:
        d[i] = 1
for i in d.keys():
    if d[i]>3:
        while d[i]>3:
            values.remove(i)
            d[i]-=1
print(values)
