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

def load_yolo():
	net = cv2.dnn.readNet("/home/akash/Downloads/Major_Project/yolov3/darknet/backup/cloth-yolov3_last.weights",
	                      "/home/akash/Downloads/Major_Project/yolov3/darknet/cfg/cloth-yolov3.cfg")
	classes = []
	with open("/home/akash/Downloads/Major_Project/yolov3/darknet/cfg/obj.names", "r") as f:
		classes = [line.strip() for line in f.readlines()]

	layers_names = net.getLayerNames()
	output_layers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
	colors = np.random.uniform(0, 255, size=(len(classes), 3))
	return net, classes, colors, output_layers


def load_image(img):
	# image loading
	#img = cv2.imread(img_path)
	img = cv2.resize(img, None, fx=0.4, fy=0.4)
	height, width, channels = img.shape
	return img, height, width, channels


def start_webcam():
	cap = cv2.VideoCapture(0)

	return cap


def display_blob(blob):
	'''
		Three images each for RED, GREEN, BLUE channel
	'''
	for b in blob:
		for n, imgb in enumerate(b):
			cv2.imshow(str(n), imgb)


def detect_objects(img, net, outputLayers):
	blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(
	    320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
	net.setInput(blob)
	outputs = net.forward(outputLayers)
	return blob, outputs


def get_box_dimensions(outputs, height, width):
	boxes = []
	confs = []
	class_ids = []
	for output in outputs:
		for detect in output:
			scores = detect[5:]
			class_id = np.argmax(scores)
			conf = scores[class_id]
			if conf > 0.3:
				center_x = int(detect[0] * width)
				center_y = int(detect[1] * height)
				w = int(detect[2] * width)
				h = int(detect[3] * height)
				x = int(center_x - w/2)
				y = int(center_y - h / 2)
				boxes.append([x, y, w, h])
				confs.append(float(conf))
				class_ids.append(class_id)
	return boxes, confs, class_ids


def draw_labels(boxes, confs, colors, class_ids, classes, img):
	indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
	font = cv2.FONT_HERSHEY_PLAIN
	for i in range(len(boxes)):
		if i in indexes:
			x, y, w, h = boxes[i]
			label = str(classes[class_ids[i]])
			color = colors[i]
			cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
			cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
	cv2.imshow("Image", img)


def image_detect(img):
    model, classes, colors, output_layers = load_yolo()
    image, height, width, channels = load_image(img)
    blob, outputs = detect_objects(image, model, output_layers)
    boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
    tmp = 0.0
    index = -1
    print(confs)
    print(boxes)
    for i in range(len(confs)):
        if(confs[i]>tmp):
            tmp = confs[i]
            index = i
    return boxes[index]
	# draw_labels(boxes, confs, colors, class_ids, classes, image)
	# while True:
	# 	key = cv2.waitKey(1)
	# 	if key == 27:
	# 		break

@app.route('/localize', methods=['POST'])
def localize_object_bbox():
    img = cv2.imdecode(numpy.fromstring(
        request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    return jsonify(image_detect(img))


if __name__ == "__main__":
    app.run(debug=True)
