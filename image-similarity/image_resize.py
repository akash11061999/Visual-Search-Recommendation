import cv2
import os
import glob

path = "/home/akash/Downloads/Major_Project/structured_images/pants/"
dest_path = "/home/akash/Downloads/Major_Project/structured_images/pants_256/"
img_list = glob.glob(path + "*.jpeg")
for item in img_list:
    img = cv2.imread(item, cv2.IMREAD_COLOR)
    new_img = cv2.resize(img, (256, 256))
    name = item.split("/")[-1]
    print(dest_path + name)
    cv2.imwrite(dest_path + name, new_img)