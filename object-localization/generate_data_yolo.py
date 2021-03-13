import json
import PIL
from PIL import Image
import os

PATH = "/home/akash/Downloads/Major_Project/meta/json/test_pairs_pants.json"
img_base_path = "/home/akash/Downloads/Major_Project/dataset/"
extension = [".jpeg", ".jpg", ".png"]

file = open(PATH, )
data = json.load(file)
print(data[0])

for item in data:
    FILE_NAME = str(item['photo']).zfill(9)
    for ext in extension:
        img_path = img_base_path + FILE_NAME + ext
        if os.path.exists(img_path):
            IMG = PIL.Image.open(img_path)
            w, h = IMG.size
            dw = 1.0/w
            dh = 1.0/h
            BBOX = item['bbox']
            x_mid = BBOX['left'] + (BBOX['width'] / 2.0)
            x_mid = x_mid*dw
            y_mid = BBOX['top'] + (BBOX['height'] / 2.0)
            y_mid = y_mid*dh
            w_norm = BBOX['width']*dw
            h_norm = BBOX['height']*dh
            file1 = open("/home/akash/Downloads/Major_Project/dataset/" + FILE_NAME + ".txt", "w")
            file1.write("0 "+str(x_mid)+" "+str(y_mid)+" "+str(w_norm)+" "+str(h_norm))
            file1.close()