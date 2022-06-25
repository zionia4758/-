import numpy as np
import pandas as pd
import sys
from scipy.stats import mode

class USER_DB:
    
    def __init__(self,x,y):
        self.DB=np.zeros((x,y))
        self.sim_mat=None
    def insert(self,x,y,value):
        self.DB[x-1][y-1]=value
    def similarity(self):
        user_DB=self.DB
        sim_mat=np.zeros((len(user_DB),len(user_DB)))
    
        for x in range(0,len(user_DB)):
            for y in range(x+1,len(user_DB)):
                a=user_DB[x,:].copy()
                b=user_DB[y,:].copy()
                common=(a!=0)*(b!=0)

                if np.any(common==True):
                    d=((4-(np.absolute((a-b)[common])   ))**2).sum()
                    
                    sim_mat[x,y]=d/(np.linalg.norm(a[common])*np.linalg.norm(b[common]))
                    sim_mat[y,x]=sim_mat[x,y]
                else:
                    sim_mat[x,y]=0
                    sim_mat[y,x]=0
        self.sim_mat=sim_mat
        #print(self.sim_mat)
        return
    def predict(self,user,item):
        user_DB=self.DB
        user_idx=user-1
        item_idx=item-1
        sim_mat=self.sim_mat[user_idx].copy()
        
        sim_mat[user_DB[:,item_idx]==0]=0
        neighbor=np.argmax(sim_mat)
        big_list=np.where(sim_mat==sim_mat[neighbor])
        result=np.average(user_DB[big_list,item_idx])
        #print(user_DB[neighbor,item_idx],neighbor,item)
        return result
        
        

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

    return DB

def preprocessing(DB):
    user_max=np.max(DB[:,0])
    item_max=np.max(DB[:,1])

    user_DB=USER_DB(user_max,item_max)
    for item in DB:
        user_DB.insert(item[0],item[1],item[2])


    return user_DB

def open_test(file_name,user_DB):
    output=[]
    with open(file_name) as f:
        for line in f.readlines():
            user,item,a,b=line.split('\t')
            user=int(user)
            item=int(item)
            output.append([user,item,user_DB.predict(user,item)])
    return output
    #print(output)

def write_output(file_name,output):
    with open(file_name,'w') as f:
        for line in output:
            f.write("{0}\t{1}\t{2}\n".format(line[0],line[1],line[2]))

def main():

    if True:
        sys_args=sys.argv
        base_file=sys_args[1]
        print("base : "+base_file)
        test_file=sys_args[2]
        print("test : "+test_file)
        output_file=test_file.replace("test","base_prediction.txt")
        print("output : "+output_file)
    else :
        base_file='u1.base'
        test_file='u1.test'
        output_file='u1.base_prediction.txt'
        
    DB=open_file(base_file)
    user_DB=preprocessing(DB)
    user_DB.similarity()
    user_DB.predict(1,10)

    output=open_test(test_file,user_DB)


    output=write_output(output_file,output)
if __name__=='__main__':
    main()
