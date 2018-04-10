import configparser
import requests
import os
import sys
import shutil
from PIL import Image

import preprocessing.convert_tf as Converter
import tensorflow as tf

class ImageController:
    def __init__(self, config):
        self.config = config

    def prepare_training(self, res, output_dir):
        image_paths = []            # store the names of all training images
        image_bytes = []            # store the byte data of all training images
        category_names = {}         # store the name of each category,
                                    # and associate it with the index of the array
        image_category_index = []   # store the (index of) each training image's
                                    # category use the category_names array to
                                    # map the category name to the index
        label_index = 0
        image_index = 0

        # for each node in a classifier, get the training data
        classifiers = res.json()['classifiers']

        for classifier in classifiers:
            nodes = classifier['nodes']
            for node_idx, node in enumerate(nodes):
                print ("Node", node_idx, ":", node['name'])
                category_names[label_index] = node['name'];
                trainingData = node['trainingData']
                for image in trainingData:
                    fname = 'storage/train/' + str(image_index) + '.jpg'
                    image_index += 1
                    response = requests.get(image, stream=True)
                    with open(fname, 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    image_paths.append(fname)
                    image_category_index.append(node_idx)
                label_index += 1

        for img_path in image_paths:
                data = tf.gfile.FastGFile(img_path, 'rb').read()
                image_bytes.append(data)

        converter = Converter.ConvertTF()
        # convert.convert_to(output_dir, image_bytes, image_category_index)
        converter.convert_to_tfrecord(output_dir, image_bytes, image_category_index)
