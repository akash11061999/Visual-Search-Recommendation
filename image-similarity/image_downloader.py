import os
import io
import pickle
#import workerpool
import urllib
import requests
from PIL import Image
import traceback
import cgi
import multiprocessing
import time

img_url_1 = []
img_url_2 = []
img_url_3 = []
img_url_4 = []
img_url_5 = []
img_url_6 = []
img_url_7 = []
img_url_8 = []
img_url_9 = []
img_url_10 = []
img_url_11 = []

def categorize_images():
    count = 0
    c2=0
    with open("/home/akash/Downloads/Major_Project/photos/photos.txt") as fp: 
        while True: 
            count += 1
            line = fp.readline()
            if not line: 
                break
            try :
                l = list(line.split(','))
                if(l[1].find("media1.modcloth")!=-1):
                    img_url_1.append((l[0], l[1].rstrip("\n")))
                elif(l[1].find("slimages.macys")!=-1):
                    img_url_2.append((l[0], l[1].rstrip("\n")))
                elif(l[1].find("g.nordstromimage")!=-1):
                    img_url_3.append((l[0], l[1].rstrip("\n")))
                elif(l[1].find("productshots")!=-1):
                    img_url_4.append((l[0], l[1].rstrip("\n")))
                elif(l[1].find("forever21")!=-1):
                    img_url_5.append((l[0], l[1].rstrip("\n")))
                elif(l[1].find("zappos")!=-1):
                    img_url_6.append((l[0], l[1].rstrip("\n")))
                elif(l[1].find("product-images")!=-1):
                    img_url_7.append((l[0], l[1].rstrip("\n")))
                elif(l[1].find("ecx.images-amazon")!=-1):
                    img_url_8.append((l[0], l[1].rstrip("\n")))
                elif(l[1].find("media.kohls")!=-1):
                    img_url_9.append((l[0], l[1].rstrip("\n")))
                elif(l[1].find("images.bloomingdales")!=-1):
                    img_url_10.append((l[0], l[1].rstrip("\n")))
                elif(l[1].find("s7d2.scene7")!=-1):
                    img_url_11.append((l[0], l[1].rstrip("\n")))
                else:
                    c2+=1
                    continue
            except:
                c2+=1
    print(count,c2)


def download_image_from_list(img_urls):
    c1 = 0
    c2 = 0
    for image in img_urls:
        if c1+c2==10:
            break
        try:
            url = str(image[1])
            fname = str(image[0])
            resp = requests.get(url)
            if resp.status_code == 200:
                c1+=1
                dataBytesIO = io.BytesIO(resp.content)
                img = Image.open(dataBytesIO)
                contentType = cgi.parse_header(resp.headers['content-type'])[0]
                extension = "." + contentType.split('/')[1]
                img.save("/home/akash/Downloads/Major_Project/"+fname+extension)
            else:
                c2+=1
        except:
            c2+=1
    print(c1, c2)



def multiprocessing_func(image):
    time.sleep(2)
    try:
        url = str(image[1])
        fname = str(image[0])
        resp = requests.get(url)
        #print(image[0], resp.status_code)
        if resp.status_code == 200:
            dataBytesIO = io.BytesIO(resp.content)
            img = Image.open(dataBytesIO)
            contentType = cgi.parse_header(resp.headers['content-type'])[0]
            extension = "." + contentType.split('/')[1]
            img.save("/home/akash/Downloads/Major_Project/dataset/"+fname+extension)
        else:
            return
    except:
        return
    
if __name__ == '__main__':
    print("Hello")
    starttime = time.time()
    processes = []
    categorize_images()
    count=0
    for image in img_url_7:
        count+=1
        if count<28000:
            continue
        if count%500==0:
            print(count)
        p = multiprocessing.Process(target=multiprocessing_func, args=(image,))
        processes.append(p)
        p.start()
        
    for process in processes:
        process.join()
         
    print('Time taken = {} seconds'.format(time.time() - starttime))

# categorize_images()

# print(len(img_url_1))
# print(len(img_url_2))
# print(len(img_url_3))
# print(len(img_url_4))
# print(len(img_url_5))
# print(len(img_url_6))
# print(len(img_url_7))
# print(len(img_url_8))
# print(len(img_url_9))
# print(len(img_url_10))
# print(len(img_url_11))
#starttime = time.time()
#download_image_from_list(img_url_3)
#print(time.time()-starttime)
