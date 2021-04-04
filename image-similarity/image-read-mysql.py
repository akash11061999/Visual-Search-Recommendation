from mysql import connector
import base64

connection = connector.connect(
    host='192.168.56.101', database='visualsearch', user='user', password='Akash123')

cursor = connection.cursor()
sql_fetch_blob_query = """SELECT * from catalog_pants"""

cursor.execute(sql_fetch_blob_query)
record = cursor.fetchall()
for row in record:
    id = row[0]
    image = row[1]
    image_name = row[2]
    print(image)
    print(id)
    print(image_name)

if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")
