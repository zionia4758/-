import numpy as np
import sys

from numpy import random
import copy







def file_open(file_name):
    DB=[]
    id_list=[]
    with open(file_name) as f:
        for lines in f.readlines():
            lines=lines.strip()
            attrs=lines.split('\t')
            attrs.append(-1)
            id_list.append(int(attrs[0]))
            attrs=list(map(float,attrs[1:]))
            DB.append(np.array(attrs))
            

    DB=np.array(DB)
    id_list=np.array(id_list)
    return DB,id_list


def count_neighbor(DB,core_point,eps):
    count=0
    neighbor=[]
    idx=0
    core_idx=-1
    for item in DB:
        dist=((item[0]-core_point[0])**2 + (item[1]-core_point[1])**2)**0.5
        if dist<=eps:
            if dist!=0:
                neighbor.append(idx)
                
            count+=1
        idx+=1
        

    
    
    return count,neighbor

def DBSCAN(DB,n,eps,minpts):
    remain_DB=DB
    cluster_id=0
    idx_list=[i for i in range(0,len(DB))]
    idx_list=np.array(idx_list)
    id=idx_list
        
    while len(remain_DB)>0:
       # print('-----')
        print(cluster_id)
        print(len(remain_DB))
        next_list=np.empty((0,3))
        rand_idx=random.randint(0,len(remain_DB))
      #  rand_idx=368
        core_point=remain_DB[rand_idx]
        DB_idx=id[rand_idx]
        #print(core_point)
      #  print(rand_idx,DB_idx)
        count,neighbor=count_neighbor(DB,core_point,eps)
        remain_DB=np.delete(remain_DB,rand_idx,axis=0)
       
        DB[DB_idx,2]=-2
      # print(DB_idx,DB[DB_idx])
       # print('=========')

        if count>=minpts:
            #print('core')
            core_point[2]=cluster_id


            n_data=DB[neighbor,:]
            n_bool=n_data[:,2]<-0.5
            DB[neighbor,2]=cluster_id

            next_list=np.append(next_list,n_data[n_bool],axis=0)

            if len(next_list)==0:
               # print("0state")
                continue
            while len(next_list)>0:
                next_core=next_list[0,:]
                next_list=np.delete(next_list,0,axis=0)
                count,neighbor=count_neighbor(DB,next_core,eps)

                if count>=minpts:
                    n_data=DB[neighbor,:]
                    n_bool=n_data[:,2]<-0.5
                    DB[neighbor,2]=cluster_id
                    next_list=np.append(next_list,n_data[n_bool],axis=0)

            cluster_id+=1
        

        DB_bool=DB[:,2]==-1
        remain_DB=DB[DB_bool]
        id=idx_list[DB_bool]

            


def output_write(DB,id_list,file_name):
    max_cluster=int(np.max(DB[:,2]))

    name=file_name.split('.')[0]+'_cluster_'
    for i in range(0,max_cluster+1):
        temp_DB=DB[DB[:,2]==i]
        #print(id_list[DB[:,2]==i])
        print(str(i)+"th cluster num :"+str(len(temp_DB)))
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
        file_name='input2.txt'
        file_open(file_name)
        n=4
        eps=2
        minpts=7
        
    DB,id_list=file_open(file_name)

    DBSCAN(DB,n,eps,minpts)
    output_write(DB,id_list,file_name)




if __name__=='__main__':
    main()
