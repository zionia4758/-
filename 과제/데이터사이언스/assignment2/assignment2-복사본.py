with open("dt_train1.txt") as f:
    data=f.read()
    data=data.replace('\t',',')
    print(data)
    f=open("dt_train_test.csv",'w')
    f.write(data)
