import numpy as np
import sys
import math

import pandas as pd


class node:
    def __init__(self):
        self.child={}
        self.attribute=""
        self.is_leaf=False
        
    def insert_child(self,data):
        self.child[data]=node()
    def select_attr(self,attr):
        self.asttribute=attr
    def leaf(self,data):
        self.is_leaf=True
        self.attribute=data


def gain(data_set):
    attr,dist=np.unique(data_set,return_counts=True)
    #print(dist)
    total=np.sum(dist)
    info_gain=0
    for i in dist:
        if i==0:
            continue

        info_gain-=(i/total)*math.log10(i/total)
    return info_gain
    
def construct_tree(node,attr,DB):
    initial_gain=gain(DB[:,-1])
    length=len(DB)
    select_attr=-1
    final_values=[]
    final_DB=[]
    tree=[]
    final_gain=9865421
    for new_attr in attr:
        attr_values=np.unique(DB[:,new_attr])
        #print(attr_values)
        part_DB=[]
        for value in attr_values:
            new_DB=DB[(DB[:,new_attr]==value),:]
            part_DB.append(new_DB)
        #print(part_DB)
        info_gain=0
        for part in part_DB:
         #   print(gain(part[:,-1]))
            info_gain+=gain(part[:,-1]) *int(len(part))/length
        #print(info_gain)
        if info_gain<final_gain:
            final_DB=part_DB
            final_gain=info_gain
            select_attr=new_attr
            final_values=attr_values
    info_gain=initial_gain-final_gain
    #print(final_DB)

    global attrs
    print(attrs[select_attr])
    print(str(select_attr))
    next_attr=attr[attr!=select_attr]
    
    print(next_attr)
    if info_gain==0 or final_gain==0:

        print(111)
        
        unique,counts=np.unique(DB[:,-1],return_counts=True)
        node.leaf(unique[np.argmax(counts)])
        
        
    else :
        node.select_attr(attrs[select_attr])
        print(final_values)
        i=0
        for part_DB in final_DB:
            print(final_values[i])
            node.insert_child(final_values[i])
            construct_tree(node.child[final_values[i]],next_attr,part_DB)
            i+=1


def printTree(node):
    print(node.attribute)
    if(node.is_leaf==True):
        return
    for c in node.child:
        print(node.child[c])

def classify(node,data_set):
    while node.is_leaf==False:
        print(node.attribute)
        



def open_file(train):
    with open(train) as f:
        attr=f.readline()
        attr=attr.strip()
        attr=attr.split('\t')
        print(attr)
        lines=f.readlines()
        
        DB=np.empty((0,len(attr)),str)
        for line in lines:
            line=line.strip()
            #print(line)
            DB=np.append(DB,np.array([line.split('\t')]),axis=0)
        print(DB)
        return attr,DB

def main():
    train_file=sys.argv[1]
    test_file=sys.argv[2]
    output_file=sys.argv[3]
    root=node()
    global attrs
    attr,DB=open_file(train_file)
    attrs=attr
    attr_num=len(attr)
    remain_attr=np.array([i for i in range(0,attr_num-1)])
    print(remain_attr)
    construct_tree(root,remain_attr,DB)

   # printTree(root)


if __name__=='__main__':
    main()
