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
            DB.append(attrs)
            DB.append(-1)

    DB=np.array(DB)
    return DB

def dist(x,y):
    return np.linalg.norm(x,y)

def count_neighbor(DB,core,eps):
    count=0
    neighbors=[]
    merge=False
    id=core[3]
    for item in DB:
        if core[0] == item[0]:
            continue
        if dist(item[1:3],core[1:3])<=eps:
            count+=1
            if item[3]==-1:
                new_pts.append(item)

    new_pts=np.array(new_pts)
    return count,new_pts

def spread(DB,eps,minpts,queue,cluster):
    for len(queue)>0:
        next=queue.pop()
        count,new_pts=count_neighbor(DB,next,eps)
        if count>=minpts:
            if len(new_pts)>0:
                new_pts[:,3]=next[3]
                queue.append(new_pts)
                

def DBSCAN(DB,n,eps,minpts):
    cluster=[]
    queue=[]
    remain_DB=DB.copy()
    cluster_id=0
    for len(remain_DB)>0:
        core_idx=random.randint(0,max_index)
        core_point=remain_DB[initial_idx]
        remain_DB=np.delete(remain_DB,initial_idx)
        temp_cluster=np.empty((0,4))
        count,new_pts=count_neighbors(DB,core_point,eps)
        if count>=minpts:
            core_point[3]=cluster_id
            queue.append(new_pts)
            new_pts[:,3]=cluster_id

            temp_cluster=np.append(temp_cluster,np.array([core_point]),axis=0)
            temp_cluster=np.append(temp_cluster,new_pts,axis=0)
            spread(DB,eps,minpts,queue,temp_cluster)
            

        cluster_id+=1

    

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
    DB=file_open(file_name)
    DBSCAN(DB.copy(),n,eps,minpts)




if __name__=='__main__':
    main()
