import lmdb
import caffe
import os
from feature_extractor import FeatureExtractor

class Indexer(object):
    def __init__(self, config):
        self.layer = config["layer"]
        self.input_layer = config["input_layer"]
        self.feature_extractor = FeatureExtractor(config["path_to_deploy_file"], config["path_to_model_file"],
                                                  input_layer_name=self.input_layer)
        #self.image_paths = image_paths

    def index_batch(self, batch_size, start_index=0, stop_index=None):
        batches = [self.image_paths[x:x + batch_size] for x in range(0, len(self.image_paths), batch_size)]
        batch_num = 0
        if not stop_index:
            stop_index = len(batches)
        batches = batches[start_index:stop_index]
        for batch in batches:
            batch_num += 1
            print("Indexing batch ", batch_num, len(batch))
            fv_dict = self.feature_extractor.extract_batch(batch, layer=self.layer)
            self.write_to_lmdb(fv_dict)
    
    def index(self, img):
        fv = self.feature_extractor.extract_from_img(img, layer=self.layer)
        return fv

    def write_to_lmdb(self, fv_dict):
        env = self.connection
        with env.begin(write=True) as txn:
            for k in fv_dict:
                txn.put(k.encode('ascii'), fv_dict[k].tostring())