import numpy as np
import sys

from numpy import random
import copy

import matplotlib.pyplot as plt





def file_open(file_name):
    DB=[]
    with open(file_name) as f:
        for lines in f.readlines():
            lines=lines.strip()
            attrs=lines.split('\t')
            attrs.append(-1)
            attrs=list(map(float,attrs[1:]))
            DB.append(np.array(attrs))
            

    DB=np.array(DB)

    return DB


def ideal_open(i,n):
    c_list=[]
    filename='input{}_cluster_{}_ideal.txt'.format(i,n)


    with open(filename) as f:
        lines=f.readlines()
        for point in lines:
            c_list.append(int(point))

    return c_list


    
def main():

    if False:
        args=sys.argv
        file_name=args[1]
        n=args[2]
        eps=args[3]
        minpts=args[4]
    else:
        file_name='input1.txt'
        file_open(file_name)

    DB=file_open(file_name)
    c=[]
    number=11
    i=1
    for n in range(0,number):
        c.append(ideal_open(i,n))
    x_values=DB[:,0]
    y_values=DB[:,1]
    color=['r','b','y','g','b','c','m','w','brown','pink','gray']
    for i in range(0,number):
        plt.scatter(x_values[c[i]],y_values[c[i]],color=color[i],s=3)
    
    plt.show()



if __name__=='__main__':
    main()
