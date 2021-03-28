import glob
import os
import sys
from new_indexer import Indexer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle


if __name__ == "__main__":
    print(sys.argv)
    args = sys.argv[1:]
    print(args)
    if len(args) < 1:
        print("Requires parameters vertical")
        sys.exit(1)
    vertical = args[0]
    print(vertical)
    base_dir = "/home/akash/Downloads/Major_Project/civr_wivr_91203/"
    lmdb_dir = "/home/akash/Downloads/Major_Project/lmdbs/"
    base_image_dir = "/home/akash/Downloads/Major_Project/structured_images/"
    config = {}
    config["layer"] = "linear_embedding_q_norm"
    config["input_layer"] = "data_q"
    config["fv_db_path"] = os.path.join(
        lmdb_dir, vertical+"_civr_wivr_91203_543750")
    config["path_to_deploy_file"] = os.path.join(
        base_dir, "visnet_deploy.prototxt")
    config["path_to_model_file"] = os.path.join(
        base_dir, "_iter_40630.caffemodel.h5")
    imdir = os.path.join(base_image_dir, vertical)
    if not os.path.exists(imdir):
        imdir = os.path.join(base_image_dir, vertical)
    image_path_1 = glob.glob(imdir + "/*.jpg")
    image_path_2 = glob.glob(imdir + "/*.jpeg")
    image_path_3 = glob.glob(imdir + "/*.png")
    print(len(image_path_1), len(image_path_2), len(image_path_3))
    image_paths = image_path_1 + image_path_2 + image_path_3
    print(len(image_paths))
    home_dir = "/home/akash/Downloads/Major_Project/"
    catalog_image_dir = os.path.join(home_dir, "structured_images/" + "pants/")
    catalog_image_paths = glob.glob(catalog_image_dir + "*.jpeg")
    #catalog_image_paths = catalog_image_paths[:100]
    indexer = Indexer(config)
    print("Finding feature vectors of catalog images")
    # catalog_image_fv_dict = indexer.index(catalog_image_paths)
    # a_file = open("fv_dict.pkl", "wb")
    # pickle.dump(catalog_image_fv_dict, a_file)
    # a_file.close()

    a_file = open("fv_dict.pkl", "rb")
    catalog_image_fv_dict = pickle.load(a_file)

    #print(catalog_image_fv_dict["000371147"])
    query_img_fv = indexer.index(["/home/akash/Downloads/Major_Project/structured_images/wtbi_pants_query_crop/000000383.jpeg"])
    print("Query Image FV------>", type(query_img_fv["000000383"]))
    query_fv = query_img_fv["000000383"]
    res = []
    for k in catalog_image_fv_dict:
        dist = np.linalg.norm(query_fv - catalog_image_fv_dict[k])
        #dist = np.dot(query_fv,catalog_image_fv_dict[k])/(np.linalg.norm(query_fv)*np.linalg.norm(catalog_image_fv_dict[k]))
        l1 = []
        l1.append(dist)
        l1.append(k)
        res.append(l1)
    res.sort()
    for i in range(0,5):
        print(res[i])