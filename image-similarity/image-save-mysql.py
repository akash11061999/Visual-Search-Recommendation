from mysql import connector
import base64
import glob
import random



BASE_DIR = "/home/akash/Downloads/Major_Project/structured_images/tops/"
img_paths = glob.glob(BASE_DIR + "*.jpeg")

connection = connector.connect(
    host='192.168.56.101', database='visualsearch', user='user', password='Akash123')

top_names = ["ZARA's Exclusive Top", "H&M Fancy Wear", "Pantaloon's Summer Top", "Nykaa Fashion Wear", "Levi's Top"]
cnt = 0
for img_path in img_paths:
    cnt = cnt%5
    image64 = ""
    with open(img_path, "rb") as img_file:
        image64 = base64.b64encode(img_file.read())
    #print(image64)
    cursor = connection.cursor()
    sql_insert_blob_query = """ INSERT INTO tops
                          (id, image, image_name, price) VALUES (%s,%s,%s,%s)"""

    img_name = top_names[cnt]
    id = img_path.split("/")[-1].split(".")[0]
    price = random.randint(100, 10000)
    print(id, img_name)
    insert_blob_tuple = (id, image64, img_name, price)
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    connection.commit()
    cnt=cnt+1

if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")
