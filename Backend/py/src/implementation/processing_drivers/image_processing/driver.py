import io
from PIL import Image
from array import array
import os
import sys
# import cv2
import tensorflow as tf

# added requests for calls to your APIs
import configparser
import requests
import shutil
from io import BytesIO

import numpy as np
import skimage.io as io

# TODO if the system said cant find module look at this next line
# (modules in different directories need to be referenced through system paths)

config = configparser.ConfigParser()
config.read('config.ini')

sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))
sys.path.append(os.path.join(os.path.dirname(__file__)))

# from implementation.storage_controller.NetworkedFileSystem.input_controller import InputController
# from implementation.storage_controller.NetworkedFileSystem.checkpoint_controller import CheckpointController
# from implementation.storage_controller.Entities.instagram_post_entity import InstagramPostEntities
# from implementation.storage_controller.TableManagers.table_manager import TableStorageConnector

from implementation.models import train_image_classifier as train
from implementation.models import eval_image_classifier as eval
from implementation.models import test_build as test
from implementation.models.datasets import convert_my as convert
from implementation.models import image_utils

class Driver:
    def __init__(self):
        # TODO: This now stored on your rest API so ignore this and make calls to routes to grab and store checkpoints
        self.checkpoint_directory = "../../../resources/checkpoints"
        # if it has been tested
        self.testvar = False

    def start_eval(self):
        # train.train("../../../resources/checkpoints/inception_v4.ckpt", self.checkpoint_directory,"../../../resources/tfrecord", logo_name=brand) #ask bryce to fix logoname
        output = eval.eval("../../../resources/train","../../../resources/train","../../../resources/tfrecord",model_name = "inception_v4",batch_size=100)
        print("eval: ", output)

    def start_classify(self):
        test.setup_then_classify("../../../resources/results/Nike")

    def start_training(self):
        print("starting driver...")


        # headers = {"Authorization": config.auth['JWT']}
        JWT = "BEARER eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlbnNvcmZsb3dAbG9nb2RldGVjdC5jb20iLCJ1c2VySWQiOiI1YWM0MTE3YTMzZDA5ODJmOGM0ZWEyNjkiLCJpYXQiOjE1MjI3OTg5ODYsImV4cCI6MTU1NDM1NjU4Nn0.y25h7mA6NWUpCq7EeecZ3FuP6IUJpougNVrl695SyAU"
        headers = {"Authorization": JWT}
        # res = requests.get(config.routes['Training'], headers=headers)
        res = requests.get("http://localhost:2000/tensorflow/training", headers=headers)

        if res.status_code == requests.codes.ok:
            print("Retrieved training images from Rest API")

            image_paths = []            # store the names of all training images
            # category_names = {}         # store the name of each category,
                                        # and associate it with the index of the array
            image_category_index = []   # store the (index of) each training image's
                                        # category use the category_names array to
                                        # map the category name to the index

            # for each node in a classifier, get the training data
            classifiers = res.json()['classifiers']

            for classifier in classifiers:
                nodes = classifier['nodes']
                label_index = 0
                image_index = 0
                for node_idx, node in enumerate(nodes):
                    # print ("Node", node_idx, ":", node['name'])
                    # category_names[label_index] = node['name'];
                    trainingData = node['trainingData']
                    for image in trainingData:
                        fname = '../../../storage/train/' + str(image_index) + '.jpg'
                        image_index += 1
                        response = requests.get(image, stream=True)
                        with open(fname, 'wb') as out_file:
                            shutil.copyfileobj(response.raw, out_file)
                        image_paths.append(fname)
                        image_category_index.append(node_idx)
                    label_index += 1
                setup_then_train(classifier['_id'], image_paths)

    def setup_then_train(self, classifier_id, image_paths):

        image_bytes = []            # store the byte data of the training images
        for img_path in image_paths:
            data = tf.gfile.FastGFile(img_path, 'rb').read()
            image_bytes.append(data)

        print("Converting to tfrecord...")

        # print(image_category_index)
        convert.convert_to("../../../resources/tfrecord", image_bytes, image_category_index)
        print("training")

        # logo name = classifierId
        train.train("../../../resources/checkpoints/inception_v4.ckpt",
            self.checkpoint_directory,
            "../../../resources/tfrecord",
            logo_name=classifier_id) #ask bryce to fix logoname

def main():
    Driver().start_training()
    # Driver().start_eval()
    # Driver().start_classify()
    # Driver().start_eval()

if __name__ == "__main__":
    main()
