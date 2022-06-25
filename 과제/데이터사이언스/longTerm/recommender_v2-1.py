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
        length=user_DB.shape[1]
        sim_mat=np.zeros((length,length))
        for x in range(0,length):
            for y in range(x+1,length):
                a=user_DB[:,x].copy()
                b=user_DB[:,y].copy()
                if np.all(a==0) or np.all(b==0):
                    sim_mat[x,y]=0
                    sim_mat[y,x]=0
                    continue
                mul=a*b
                if np.all(mul==0):
                    sim_mat[x,y]=0
                    sim_mat[y,x]=0
                    continue
                
                bool_index=(mul!=0)
                
                
                sim_mat[x,y]=np.sum(mul)/(np.linalg.norm(a[bool_index])*np.linalg.norm(b[bool_index]))
                sim_mat[y,x]=sim_mat[x,y]
        self.sim_mat=sim_mat
        #print(self.sim_mat)
        return
    def predict(self,user,item):
        user_DB=self.DB
        user_idx=user-1
        item_idx=item-1

        ###새로운 user나 item처리 
        if user >=len(user_DB):
            #print(item_idx)
            val_list=user_DB[:,item_idx]
            valid_list=val_list[val_list!=0]
            mode_val=mode(valid_list)
            return mode_val
        if item >=len(user_DB[0]):
            print('new item')
            return 3



        rating=user_DB[user_idx,:]
        non_zero_sim=self.sim_mat[rating!=0,item_idx]
        non_zero_rating=rating[rating!=0]
        max_val_index=np.argmax(non_zero_sim)
        result=non_zero_rating[max_val_index]

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
    
    if False:
        sys_args=sys.argv
        base_file=sys_args[1]

        test_file=sys_args[2]

        

    else :
        base_file='u1.base'
        test_file='u1.test'



    print("base : "+base_file)
    DB=open_file(base_file)
    
    
    user_DB=preprocessing(DB)
  #  print("sim cal start")
    user_DB.similarity()
   # print("sim cal end")

    print("test : "+test_file)
    output=open_test(test_file,user_DB)

    output_file=test_file.replace("test","base_prediction.txt")
    print("output : "+output_file)
    output=write_output(output_file,output)
if __name__=='__main__':
    main()
