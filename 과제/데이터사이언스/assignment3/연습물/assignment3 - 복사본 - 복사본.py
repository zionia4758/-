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

    return DB


def count_neighbor(DB,core_point,eps):
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
        

    
    
    return count,neighbor

def DBSCAN(DB,n,eps,minpts):
    remain_DB=DB[ DB[:,2]==-1]
    cluster_id=0
    while len(remain_DB)>0:
        print(len(remain_DB))
        print(cluster_id)
        next_list=np.empty((0,3))
        rand_idx=random.randint(0,len(remain_DB))
        #rand_idx=0
        
        core_point=DB[rand_idx]
        core_point[2]=-2
        print(core_point)
        count,neighbor=count_neighbor(DB,core_point,eps)
        #print(neighbor)

        if count>=minpts:
            core_point[2]=cluster_id
            print(core_point[2])
            #print(neighbor)
            neighbor_list=DB[neighbor]
             
            next_neighbor=neighbor_list[neighbor_list[:,2]<-0.5]
            DB[neighbor,2]=cluster_id
            #print(neighbor)
            next_list=np.append(next_list,next_neighbor,axis=0)
            if len(next_list)==0:
                continue

        
            while len(next_list)>0:
                #print(len(next_list))
                next_core=next_list[0]
                #print(next_core)
                next_list=np.delete(next_list,0,axis=0)
                count,neighbor=count_neighbor(DB,next_core,eps)
                if count>=minpts:   
                    neighbor_list=DB[neighbor]
             
                    next_neighbor=neighbor_list[neighbor_list[:,2]<-0.5]
                    DB[neighbor,2]=cluster_id


                    next_list=np.append(next_list,next_neighbor,axis=0)
            
            cluster_id+=1
        
        



        remain_DB=DB[ DB[:,2]==-1]
        if len(remain_DB)==1:
            print(remain_DB)
            return

def output_write(DB,file_name):
    max_cluster=int(np.max(DB[:,2]))
    
    id_list=[i for i in range(0,len(DB))]
    id_list=np.array(id_list)
    name=file_name.split('.')[0]+'_cluster_'
    for i in range(0,max_cluster+1):
        temp_DB=DB[DB[:,2]==i]
        #print(id_list[DB[:,2]==i])
        print(len(temp_DB))
        with open(name+str(i)+'_ideal.txt','w') as f:
            for item in id_list[DB[:,2]==i]:
                f.write(str(item)+'\n')
             


    
def main():

    if False:
        args=sys.argv
        file_name=args[1]
        n=args[2]
        eps=args[3]
        minpts=args[4]
    else:
        file_name='input3.txt'
        file_open(file_name)
        n=4
        eps=5
        minpts=5
    DB=file_open(file_name)

    DBSCAN(DB,n,eps,minpts)
    output_write(DB,file_name)




if __name__=='__main__':
    main()
