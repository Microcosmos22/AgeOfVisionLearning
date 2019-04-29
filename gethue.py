f = open("huetoslpnumber.txt", "a+")

for i in range (0,5312):
    line = str(i)+"\t"+str(float(i)/5312)+"\n"
    #print(line)
    
    f.write(line)