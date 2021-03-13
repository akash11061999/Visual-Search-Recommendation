import glob
import os

current_dir = '/home/akash/Downloads/Major_Project/dataset/'

# Percentage of images to be used for the test set
percentage_test = 10
counter = 1
index_test = round(100 / percentage_test)

# Create and/or truncate train.txt and test.txt
file_train = open('/home/akash/Downloads/Major_Project/train.txt', 'w')
file_test = open('/home/akash/Downloads/Major_Project/test.txt', 'w')

l3 = glob.glob(current_dir + "*.txt")

for item in l3:
    if counter == index_test:
        counter = 1
        item = item[:-4]
        for ext in [".jpeg", ".png", ".jpg"]:
        	if os.path.exists(item + ext):
        		file_test.write(item + ext + "\n")
        		break
    else:
        item = item[:-4]
        for ext in [".jpeg", ".png", ".jpg"]:
        	if os.path.exists(item + ext):
        		file_train.write(item + ext + "\n")
        		break
        counter = counter + 1

file_test.close()
file_train.close()
