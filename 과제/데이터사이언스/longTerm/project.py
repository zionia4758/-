import numpy as np
import pandas as pd
class user:
    def __init__(self):
        self.item_list=[]
        self.score_list=[]

    def insert(self,item,score):
        self.item_list.append(item)
        self.score_list.append(score)



def open_file2(file_name):
    users={}
    max_item=0
    with open(file_name) as f:
        for line in f.readlines():
            user_id,item,score,a =line.split('\t')
            user_id=int(user_id)
            item=int(item)
            score=int(score)
            if not user_id in users:
                users[user_id]=user()
                
            users[user_id].insert(item,score)
            max_item=max(max_item,item)
    return users,max_item

def open_file(file_name):
    DB=[]
    with open(file_name) as f:
        for line in f.readlines():
            user_id,item,score,a =line.split('\t')
            user_id=int(user_id)
            item=int(item)
            score=int(score)
            DB.append([user_id,item,score])
            
    DB=np.array(DB)
    user_list=np.unique(DB[:,0])
    item_list=np.unique(DB[:,1])
    return DB, user_list,item_list

def preprocessing(DB,user_list,item_list):
    user_DB=np.zeros((len(user_list),len(item_list)))
    for item in DB:
        u_idx=np.where(user_list==item[0])[0]
        i_idx=np.where(item_list==item[1])[0]
        user_DB[u_idx,i_idx]=item[2]

    return user_DB

def similarity(user_DB,user_list):
    sim_mat=np.zeros((len(user_list),len(user_list)))
    for x in range(0,len(user_list)):
        for y in range(x+1,len(user_list)):
            a=user_DB[x,:]
            b=user_DB[y,:]
            sim_mat[x,y]=(a@b)/(np.linalg.norm(a)*np.linalg.norm(b))
            sim_mat[y,x]=sim_mat[x,y]
            
    return sim_mat

def predict(user_DB,sim_mat,item


def main():
    DB,user_list,item_list=open_file('u1.base')
    user_DB=preprocessing(DB,user_list,item_list)
    df=pd.DataFrame(user_DB,index=user_list, columns=item_list)
    sim_mat=similarity(user_DB,user_list)

if __name__=='__main__':
    main()
