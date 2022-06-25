import sys
import numpy as np
import string









def open_file(input_txt):
    global max_val,min_val
    file = open(input_txt , 'r')
    lines=file.readlines()
    index=0
    DB=[]
    max_val=None
    min_val=None
    for line in lines:
        line=line.strip()
        data=list(map(int,line.split("\t")))
        if max_val==None:
            max_val=max(data)
        else:
            max_val=max(max_val,max(data))
        if min_val==None:
            min_val=min(data)
        else:
            min_val=min(min_val,min(data))
        index+=1
        
        DB.append(np.array(data))


    #DB.append(index)
    print("max :"+str(max_val)+", min : "+str(min_val))
    file.close()
    return DB,max_val,min_val

def save_file(output_txt,data):
    file=open(output_txt, 'w')
    file.write(data)
    file.close()


def candidate_init(DB):
    candidate=np.array([[i] for i in range(min_val,max_val+1)])
    candi_count=np.zeros(max_val-min_val+1)
   # print(candidate )
    #print(candi_count)
    return candidate,candi_count


def frequent_check(DB, min_sup, candidate,candi_count):
    DB_length=len(DB)
    for dataset in DB:
        for i in range(0,len(candidate)):
            candi=candidate[i]
            #print(candi,dataset)
            bool_arr=np.isin(candi,dataset)
            #print(bool_arr)
            if(np.all(bool_arr==True)):
                candi_count[i]+=1
    bool_index=((candi_count/DB_length*100)>=min_sup)
    #print(candi_count/DB_length*100)
    #print(bool_index)
    L_list=candidate[bool_index]
    L_counts=candi_count[bool_index]

    #print(L_list)
    if len(L_list)>0:
        return L_list,L_counts
    else:
        return None,None

def build_candidate(L,num):
    length=len(L)
    candidate=[]
    #print(L)
    for i in range(0,length):
        for j in range(i+1,length):
            new_candi=np.concatenate((L[i],L[j]))
            new_candi=np.unique(new_candi)
            if len(new_candi) != num+1:
                continue
            candidate.append(new_candi)
            #print(new_candi)
    need_cnt=num*(num+1)/2
    candi=np.array(candidate)
    candi,counts=np.unique(candidate,axis=0,return_counts=True)
    #print(need_cnt)
    #print((counts==need_cnt))
    #print(candi)
    ret_candidate = candi[(counts==need_cnt)]
    #print(ret_candidate)
    return ret_candidate

def print_list(L,L_counts):
    global output_string
    global DB_len
    for i in range(0,len(L)):
        print(L[i],round(L_counts[i]/DB_len*100,2))
        #print(L[i], L_counts[i])

def confidence_cal(L_list):
    max_item=len(L_list)
    confidence_list=[]
    if max_item >=2:
        for i in range(1,max_item):

            for j in range(0,i):
                left=L_list[j]
                right=L_list[i]
                left_index=0
                for left_itemset in left[0]:
                    right_index=0
                    for right_itemset in right[0]:
                        if np.all(np.isin(left_itemset, right_itemset))==True:
                            assoc_set=np.setdiff1d(right_itemset,left_itemset,assume_unique = True)
                            left_sup=left[1][left_index]
                            right_sup=right[1][right_index]
                            #print(left_itemset)
                            #print(assoc_set)
                            #print(right_itemset)
                            
                            #print(left_sup,right_sup)   
                            confidence_list.append([left_itemset,assoc_set,left_sup,right_sup])


                        right_index+=1
                    left_index+=1
    #print(confidence_list)
    return confidence_list

def np_array_format(np_array):
    string="{"
    for a in np_array:
       # print(a)
        if string=="{":
            string+=str(a)
        else:
            string+=",{0}".format(str(a))
    string+="}"
    return string

def make_output(confidence_list):
    num=len(confidence_list)
    outputString=""
    global DB_len

    for list_set in confidence_list:
        
        support=np.round(list_set[3]/DB_len*100,2)
        confidence=np.round(list_set[3]/list_set[2]*100,2)
        outputString += "{0}\t{1}\t{2:.2f}\t{3:.2f}\n".format(np_array_format(list_set[0]),
                                                           np_array_format(list_set[1]),support,confidence)
        #print(outputString)
    
    return outputString

def main():
    global output_string
    output_string=""
    print(len(sys.argv))
    if(len(sys.argv)!=4):
        raise Exception("충분하지 않은 인자 개수\n")
    min_sup=int(sys.argv[1])
    input_f=sys.argv[2]
    output_f=sys.argv[3]
    print("Input file : {0} , output file : {1}".format(input_f,output_f))

    DB,max_val,min_val= open_file(input_f)

    global DB_len
    DB_len=len(DB)

    candidates=[]
    candidate,candi_count=candidate_init(DB)
    candidates.append([candidate,candi_count])
    num=0
    L_list=list()
    L,L_counts=frequent_check(DB,min_sup,candidates[num][0],candidates[num][1])
    L_list.append([L,L_counts])
    print_list(L,L_counts)
    #print(L)
    while L is not None:
        num+=1
        new_candidate=build_candidate(L,num)
        new_candi_count=np.zeros(len(new_candidate))
        #print(len(new_candidate),len(new_candi_count))
        candidates.append([new_candidate,new_candi_count])
        #print(candidates[1])
        L,L_counts=frequent_check(DB,min_sup,candidates[num][0],candidates[num][1])
        if L is not None:
            print_list(L,L_counts)
            L_list.append([L,L_counts])

    confidence_list=confidence_cal(L_list)
    
    output_string=make_output(confidence_list)
    print(output_string)
    save_file(output_f,output_string)




if __name__=='__main__':
    main()
