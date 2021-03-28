import numpy as np
from flask import Flask, request, jsonify, render_template
import glob
import os
import sys
from new_indexer import Indexer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from PIL import Image
import numpy
import cv2
from mysql import connector
import base64
import glob

app = Flask(__name__)
catalog_image_fv_dict = pickle.load(open("fv_dict.pkl", "rb"))

BASE_DIR = "/home/akash/Downloads/Major_Project/civr_wivr_91203/"


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/catalogImage/<image_id>', methods=['GET'])
def read_image(image_id):
    #return(image_id)
    connection = connector.connect( host='192.168.56.101', database='visualsearch', user='user', password='Akash123')
    cursor = connection.cursor()
    sql_fetch_blob_query = """SELECT * from catalog_tops WHERE id=%s"""

    cursor.execute(sql_fetch_blob_query, (image_id, ))
    record = cursor.fetchall()
    res = []
    for row in record:
        id = row[0]
        image = row[1]
        image_name = row[2]
        # print(image)
        print(id)
        # print(image_name)
        res = [id, image_name, image]

    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
    
    return(res[2])


def generate_config(base_dir):
    config = {}
    config["layer"] = "linear_embedding_q_norm"
    config["input_layer"] = "data_q"
    config["path_to_deploy_file"] = os.path.join(
        base_dir, "visnet_deploy.prototxt")
    config["path_to_model_file"] = os.path.join(
        base_dir, "_iter_10000.caffemodel.h5")
    return config


def compute_fv_image(img):
    indexer = Indexer(generate_config(BASE_DIR))
    return indexer.index(img)


@app.route('/predict', methods=['POST'])
def predict():
    # print(request.files['file'])
    img = cv2.imdecode(numpy.fromstring(
        request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    query_img_fv = compute_fv_image(img)

    a_file = open(
        "/home/akash/Downloads/Major_Project/fv_dict_tops_10000.pkl", "rb")
    catalog_image_fv_dict = pickle.load(a_file)

    res = []
    for k in catalog_image_fv_dict:
        dist = np.linalg.norm(query_img_fv - catalog_image_fv_dict[k])
        l1 = []
        l1.append(dist)
        l1.append(k)
        res.append(l1)
    res.sort()
    ans = []
    for i in range(0, 5):
        ans.append(res[i][1])
    images = []
    for img_id in ans:
        images.append(read_image(img_id))
    return (jsonify(images))


@app.route('/results', methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)
