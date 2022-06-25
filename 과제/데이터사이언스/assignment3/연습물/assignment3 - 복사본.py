import numpy as np
import sys

from numpy import random
import copy







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
    count_DB=np.zeros(len(DB))
   # print(DB)
    neighbor_DB=[[] for i in range(len(DB))]

    return DB,count_DB,neighbor_DB


def count_neighbor(DB,core_point,eps,minpts,cluster_id):
    count=0
    neighbor=[]
    idx=0
    for item in DB:
        dist=((item[0]-core_point[0])**2 + (item[1]-core_point[1])**2)**0.5

        if dist<=eps:
            if dist!=0:
                neighbor.append(idx)
        count+=1
        idx+=1
            
    neighbor=DB[neighbor]
    print(neighbor)


    
    if count>=minpts:
        neighbor=neighbor[neighbor[:,2]<-0.5]
        neighbor[:,2]=cluster_id
    
    return count,neighbor


def DBSCAN(DB,n,eps,minpts):
    remain_DB=DB[ DB[:,2]==-1]
    cluster_id=0
    while len(remain_DB)>0:
        next_list=np.empty((0,3))
        rand_idx=random.randint(0,len(remain_DB))
        core_point=DB[rand_idx]
        count,neighbor=count_neighbor(DB,core_point,eps,minpts,cluster_id)
        #print(neighbor)
        if count>=minpts:
            core_point[2]=cluster_id
            if len(neighbor)>0:
                next_list=np.append(next_list,neighbor,axis=0)

            
        
            while len(next_list)>0:
                #print(len(next_list))
                next_core=next_list[0]
                print(next_core)
                next_list=np.delete(next_list,0,axis=0)
                count,neighbor=count_neighbor(DB,next_core,eps,minpts,cluster_id)
                if len(neighbor)>0:
                    next_list=np.append(next_list,neighbor,axis=0)
                #print(next_list)

            cluster_id+=1
        
        else:
            core_point[2]=-2


        remain_DB=DB[ DB[:,2]==-1]



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
        n=5
        eps=5
        minpts=5
    DB,count_DB,neighbor_DB=file_open(file_name)

    DBSCAN(DB,n,eps,minpts)




if __name__=='__main__':
    main()
