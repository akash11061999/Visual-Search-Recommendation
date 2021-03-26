import csv
import os

file = open("/home/akash/Downloads/Major_Project/triplet.csv", "r")
file1 = open("/home/akash/Downloads/Major_Project/triplet_q.txt", "w")
file2 = open("/home/akash/Downloads/Major_Project/triplet_p.txt", "w")
file3 = open("/home/akash/Downloads/Major_Project/triplet_n.txt", "w")

dataset = file.readlines()
print(len(dataset))
count = 0

for data in dataset:
    count+=1
    l = list(data.split(","))
    print(count, len(l))
    if (os.path.exists(l[0]) and os.path.exists(l[1]) and os.path.exists(l[2])):
        file1.write(l[0]+"\n")
        file2.write(l[1]+"\n")
        file3.write(l[2]+"\n")

file1.close()
file2.close()
file3.close()