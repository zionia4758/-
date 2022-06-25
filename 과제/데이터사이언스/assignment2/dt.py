import numpy as np
import sys
import math
import copy


class node:
    def __init__(self):
        self.child={}
        self.attribute=""
        self.is_leaf=False
        self.value=""
        self.distribution
        
    def insert_child(self,data):
        self.child[data]=node()
    def select_attr(self,attr):
        self.attribute=attr
    def leaf(self,data):
        self.is_leaf=True
        self.value=data
    def distribution(self,data):
        self.distribution=data

def gain(data_set):
    attr,dist=np.unique(data_set,return_counts=True)

    total=np.sum(dist)
    info_gain=0
    for i in dist:
        if i==0:
            continue
        info_gain-=(i/total)*math.log10(i/total)
    #print(dist)
    #print(info_gain)
    return info_gain

def majority(dist):
    #print(dist)
    unique,counts=np.unique(dist,return_counts=True)
    max_val=max(counts)
    check=False
    for data in dist:
        if data==max_val:
            if check==False:
                check=True
            else:
                return False
    result=unique[np.argmax(counts)]
    return result
    
def construct_tree(node,attribute,DB):
    global attr_list

    unique,dist=np.unique(DB[:,-1],return_counts=True)
   # tree.value=majority(DB[:,-1])
    if len(unique)==1:
       # print(unique)
        node.leaf(unique[0])
        return True
    node.distribution(dist)
    root_gain=gain(DB[:,-1])
    
    remain_attr=copy.deepcopy(attribute)
    DB_len=len(DB)
    attr_dic={}
    

    min_gain=987654321
    select_attr=None
    select_part_DB=None
    select_index=None
    
  #  print(remain_attr)
    #print(DB)

    for attr in remain_attr:
        part_gain=0
        index=remain_attr[attr]
        attr_values=attr_list[attr]
        
#        print(attr)
        #print(attr_values)


        #attr의 value들로 partition하며 gain총합 구하기
        for attr_value in attr_values:
            partitioned_DB=DB[(DB[:,index]==attr_value)]
            
            #print(len(partitioned_DB) ,len(DB))
            #분류되지않는 value가 있으면 majority로 보내기
            if len(partitioned_DB)==0:
           #     print("cant")
                part_gain=root_gain
                break
            
            part_gain+=gain(partitioned_DB[:,-1])*len(partitioned_DB)/DB_len
       # print(part_gain)
        attr_dic[attr]=part_gain
        
        
   # print(attr_dic)
   # print(min(attr_dic))
    select_attr=min(attr_dic,key=attr_dic.get)
    select_index=attribute[select_attr]
    del remain_attr[select_attr]
  #  print("attr select : "+select_attr)
  #  print(attr_dic)

    if root_gain==attr_dic[select_attr]:
        major=majority(DB[:,-1])
        if major==False:
            return False
    #    print("leaf")
        node.leaf(major)
        return True
    else:
        i=0
        for value in attr_list[select_attr]:
       #     print(value)
 #           print(i)
            i+=1
            partitioned_DB=DB[DB[:,select_index]==value]
            node.insert_child(value)
            #print(partitioned_DB)
            if construct_tree(node.child[value],remain_attr,partitioned_DB)==False:
                major=majority(DB[:,-1])
                if major==False:
                    return False
                else :
        #            print("leaf")
                    node.leaf(major)
                    return True
       # print("child")
       # print(node.child)
        node.select_attr(select_attr)
        return True

            
    


        

def classify(node,data_set):
    global attribute
    while node.is_leaf==False:
        select=data_set[attribute[node.attribute]]
        node=node.child[select]

    #print(node.value)
    return node.value



def open_file(train):
    print("train_data open")
    with open(train) as f:
        attr=f.readline()
        attr=attr.strip()
        attr=attr.split('\t')
        attribute={}
        attrs=attr
        i=0
        for a in attr[:-1]:
            attribute[a]=i
            i+=1
     #   print(attribute)
        lines=f.readlines()
        
        DB=np.empty((0,len(attr)),str)
        for line in lines:
            line=line.strip()
            #print(line)
            DB=np.append(DB,np.array([line.split('\t')]),axis=0)
      #  print(DB)
      #  print("-------")
    global attr_list
    attr_list={}
    for attr in attribute:
        attr_list[attr]=np.unique(DB[:,attribute[attr]])
    
    return attribute,DB,attrs
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
        
   # print(test_data)
   # print("-------")
    
    return test_data

def output_write(attribute,output,test,data):
    print("result write")
    f=open(output,'w')
   # print(attribute)
    string=""
    for attr in attribute:
        string+=attr+'\t'
    string+='\n'
    for index in range(0,len(test)):
        line=test[index]
        for one in line:
            string+=one+'\t'
        string+=str(data[index]+'\n')
    print(string)
    f.write(string)

    
def main():
    train_file=sys.argv[1]
    test_file=sys.argv[2]
    output_file=sys.argv[3]
    root=node()
    global attribute
    attribute,DB,all_attr=open_file(train_file)
    test_data=open_test(test_file)

    attr_num=len(attribute)
    print()
    construct_tree(root,attribute,DB)



    test=['31...40','low','no','fair']

    result=[]


    for data in test_data:
        result.append(classify(root,data))
        
    output_write(all_attr,output_file,test_data,result)
   # printTree(root)


if __name__=='__main__':
    main()
