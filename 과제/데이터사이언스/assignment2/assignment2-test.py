import numpy as np
import sys
import math
import copy


class node:
    def __init__(self):
        self.child={}
        self.attribute=""
        self.is_leaf=False
        
    def insert_child(self,data):
        self.child[data]=node()
    def select_attr(self,attr):
        self.attribute=attr
    def leaf(self,data):
        self.is_leaf=True
        self.attribute=data


def gain(data_set):
    attr,dist=np.unique(data_set,return_counts=True)

    total=np.sum(dist)
    info_gain=0
    for i in dist:
        if i==0:
            continue
        info_gain-=(i/total)*math.log10(i/total)
   # print(dist)
   # print(info_gain)
    return info_gain
    
def construct_tree(node,attribute,DB):
    global attr_list
    root_gain=gain(DB[:,-1])

    select_attr=-1
    remain_attr=copy.deepcopy(attribute)
    DB_len=len(DB)
    attr_dic={}
    

    min_gain=987654321
    select_attr=None
    select_part_DB=None
    select_index=None
    
    print(remain_attr)
    #print(DB)

    for attr in remain_attr:
        part_gain=0
        index=remain_attr[attr]
        attr_values=attr_list[attr]
        
        print(attr)
        print(attr_values)


        #attr의 value들로 partition하며 gain총합 구하기
        for attr_value in attr_values:
            partitioned_DB=DB[(DB[:,index]==attr_value)]
            #분류되지않는 value가 있으면 majority로 보내기
            if len(partitioned_DB)==0:
                print("cant")
                part_gain=root_gain
                break
            print(len(partitioned_DB) ,len(DB))
            part_gain+=gain(partitioned_DB[:,-1])*len(partitioned_DB)/DB_len
        attr_dic[attr]=part_gain
        print(part_gain)
    
  #  print(attr_dic)
   # print(min(attr_dic))
    select_attr=min(attr_dic)
    print("attr select : "+select_attr)
    
    if root_gain==attr_dic[select_attr]:
        ##majority voting
        print("make leaf")
        print(DB)
        values,counts=np.unique(DB[:,-1],return_count=True)
        node.leaf(values[np.argmax[counts]])
        return
    else:
        print("make child")
        attr_values=np.unique(DB[:,remain_attr[select_attr]])
        index=remain_attr[select_attr]
        del remain_attr[select_attr]
        node.select_attr(select_attr)
        for attr_value in attr_values:
            print("child attr_value "+attr_value)
            node.insert_child(attr_value)
            partitioned_DB=DB[(DB[:,index]==attr_value)]
            if gain(partitioned_DB[:,-1])==0:
                print("h part")
                print(partitioned_DB)
                node.child[attr_value].leaf(partitioned_DB[0,-1])
                continue
            if construct_tree(node.child[attr_value],remain_attr,partitioned_DB)==False:
                a=1
                

            
    

def printTree(node):
    print(node.attribute)
    if(node.is_leaf==True):
        print(node.attribute)
        return
    for c in node.child:
        print(node.child)
        print(c)
        printTree(node.child[c])
        

def classify(node,data_set):
    global attribute
    while node.is_leaf==False:

        select=data_set[attribute[node.attribute]]
        node=node.child[select]

    print(node.attribute)
        



def open_file(train):
    print("train_data open")
    with open(train) as f:
        attr=f.readline()
        attr=attr.strip()
        attr=attr.split('\t')
        attribute={}
        i=0
        for a in attr[:-1]:
            attribute[a]=i
            i+=1
        print(attribute)
        lines=f.readlines()
        
        DB=np.empty((0,len(attr)),str)
        for line in lines:
            line=line.strip()
            #print(line)
            DB=np.append(DB,np.array([line.split('\t')]),axis=0)
        print(DB)
        print("-------")
    global attr_list
    attr_list={}
    for attr in attribute:
        attr_list[attr]=np.unique(DB[:,attribute[attr]])
    print(attr_list)
    return attribute,DB
def open_test(test):
    print("test_data open")
    with open(test) as f:
        attr=f.readline()
        attr=attr.strip()
        attr=attr.split('\t')

        test_data=np.empty((0,len(attr)),str)

        lines=f.readlines()
        for line in lines:
            line=line.strip()
            test_data=np.append(test_data,np.array([line.split('\t')]),axis=0)
        
    print(test_data)
    print("-------")
    
    return test_data

def main():
    train_file=sys.argv[1]
    test_file=sys.argv[2]
    output_file=sys.argv[3]
    root=node()
    global attribute
    attribute,DB=open_file(train_file)
    test_data=open_test(test_file)

    attr_num=len(attribute)
    construct_tree(root,attribute,DB)

    print("Tree -------")
    printTree(root)
    print("----")

    test=['31...40','low','no','fair']


    
    for data in test_data:
        classify(root,data)

    
   # printTree(root)


if __name__=='__main__':
    main()
