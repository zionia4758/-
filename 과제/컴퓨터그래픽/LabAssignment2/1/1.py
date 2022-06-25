import numpy as np

a= np.arange(2,27)
print(a,'\n')

a=a.reshape(5,5)
print(a,'\n')

a[1:-1, 1:-1]=0
print(a,'\n')

a=a@a
print(a,'\n')

b=np.sum(np.square(a[0,0:5]))
b=np.sqrt(b)
print(b,'\n')
