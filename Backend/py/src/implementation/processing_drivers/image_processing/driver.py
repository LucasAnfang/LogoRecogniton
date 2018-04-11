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
import pathlib
import json

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

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Driver:
    def __init__(self):
        # TODO: This now stored on your rest API so ignore this and make calls to routes to grab and store checkpoints
        self.checkpoint_directory = "../../../resources/checkpoints/inception_v4.ckpt"
        self.train_directory = "../../../resources/train"
        # if it has been tested
        self.testvar = False

    def swap_out_checkpoints(self, prev, next):
        def clear_dir(name):
            for the_file in os.listdir(name):
                file_path = os.path.join(name, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
        def swap_dir(prev, next):
            for the_file in os.listdir(next):
                file_path = os.path.join(next, the_file)
                try:
                    if os.path.isfile(file_path):
                        shutil.move(file_path, prev)
                except Exception as e:
                    print(e)
        if os.path.isdir(prev) and os.path.isdir(next):
            clear_dir(prev)
            swap_dir(prev,next)
            clear_dir(next)
        else:
            print("one of these faild")

    def start_eval(self, classifier_ids):
        print("evaulating classifier accuracies")
        for classifier_id in classifier_ids:
            # print (classifier_id)
            output = eval.eval("../../../resources/train","../../../resources/train","../../../resources/tfrecord",logo_name=classifier_id,model_name = "inception_v4",batch_size=100)
            print("eval: ", output)

    def get_classify_images(self):
        # headers = {"Authorization": config.auth['JWT']}
        JWT = "BEARER eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlbnNvcmZsb3dAbG9nb2RldGVjdC5jb20iLCJ1c2VySWQiOiI1YWM0MTE3YTMzZDA5ODJmOGM0ZWEyNjkiLCJpYXQiOjE1MjI3OTg5ODYsImV4cCI6MTU1NDM1NjU4Nn0.y25h7mA6NWUpCq7EeecZ3FuP6IUJpougNVrl695SyAU"
        headers = {"Authorization": JWT, 'Content-Type': 'application/json'}
        # res = requests.get(config.routes['Training'], headers=headers)
        res = requests.get("http://localhost:2000/tensorflow/classify", headers=headers)

        dataset_ids = []

        if res.status_code == requests.codes.ok:
            print("Retrieved classification images from Rest API")

            for dataset in res.json()['datasets']:
                dataset_ids.append(dataset["_id"])
                image_paths = []
                for classifier in dataset['classifiers']:
                    print(classifier)

                for image in dataset['images']:
                    response = requests.get(image['url'])
                    img = Image.open(BytesIO(response.content))
                    if img.format == 'JPEG':
                        pathlib.Path('../../../storage/classify/').mkdir(parents=True, exist_ok=True)
                        fname = '../../../storage/classify/' + str(image['_id']) + '.jpg'
                        with open(fname, 'wb') as out_file:
                            shutil.copyfileobj(BytesIO(response.content), out_file)
                        image_paths.append(fname)
                self.start_classify(image_paths)

    def start_classify(self, image_paths):
        nameMap = []
        with open("../../models/class_list.txt", "r") as ins:
            for line in ins:
                nameMap.append(line.split('\n')[0])
        print(image_paths)
        # image_paths


        # if res.status_code == requests.codes.ok:
        #     print("Retrieved classification images from Rest API")
        #
        #     for dataset in res.json()['datasets']:
        #         for classifier in dataset['classifiers']:
        #             print("Loading classifiers")
        #             print ("classifierId:", classifier)
        #
        #         for image in dataset['images']:
        #             print (image)
                    # response = requests.get(image)
                    # img = Image.open(BytesIO(response.content))

                    # if img.format == 'JPEG':
                    #     pathlib.Path('../../../storage/classify/').mkdir(parents=True, exist_ok=True)
                    #     fname = '../../../storage/classify/' +  + '.jpg'
                    #     with open(fname, 'wb') as out_file:
                    #         shutil.copyfileobj(BytesIO(response.content), out_file)
                    #
                    #     image_index += 1
                    #     image_paths.append(fname)
                    #     image_category_index.append(node_idx)

            # test.setup_then_classify("../../../resources/to_classify/"+classifierId)
        # test.setup_then_classify("../../../resources/results/Nike")

    def get_training_images(self):
        print("starting driver...")


        # headers = {"Authorization": config.auth['JWT']}
        JWT = "BEARER eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlbnNvcmZsb3dAbG9nb2RldGVjdC5jb20iLCJ1c2VySWQiOiI1YWM0MTE3YTMzZDA5ODJmOGM0ZWEyNjkiLCJpYXQiOjE1MjI3OTg5ODYsImV4cCI6MTU1NDM1NjU4Nn0.y25h7mA6NWUpCq7EeecZ3FuP6IUJpougNVrl695SyAU"
        headers = {"Authorization": JWT, 'Content-Type': 'application/json'}
        # res = requests.get(config.routes['Training'], headers=headers)
        trainingUrl = "http://localhost:2000/tensorflow/training"
        res = requests.get(trainingUrl, headers=headers)

        if res.status_code == requests.codes.ok:
            print("Retrieved training images from Rest API")

            image_paths = []            # store the names of all training images
            image_bytes = []            # store the bytes of all training images
            classifier_ids = []         # store the id of each classifier for use later
            category_names = {}         # store the name of each category,
                                        # and associate it with the index of the array
            image_category_index = []   # store the (index of) each training image's
                                        # category use the category_names array to
                                        # map the category name to the index

            # for each node in a classifier, get the training data
            classifiers = res.json()['classifiers']

            label_index = 0
            image_index = 0
            # print (classifiers)
            for classifier_idx, classifier in enumerate(classifiers):
                classifier_ids.append(classifier["_id"])
                # print(classifier["_id"], classifier_ids[classifier_idx])
                for node_idx, node in enumerate(classifier['nodes']):
                    # category_names[label_index] = node['name'];
                    label_index += 1
                    for image in node['trainingData']:
                        # print (image)
                        response = requests.get(image)
                        img = Image.open(BytesIO(response.content))

                        if img.format == 'JPEG':
                            pathlib.Path('../../../storage/train/').mkdir(parents=True, exist_ok=True)
                            fname = '../../../storage/train/' + str(image_index) + '.jpg'
                            with open(fname, 'wb') as out_file:
                                shutil.copyfileobj(BytesIO(response.content), out_file)

                            image_index += 1
                            image_paths.append(fname)
                            image_category_index.append(node_idx)

                # train each classifier
                print("training", classifier['_id'])
                self.start_training(classifier['_id'], image_paths, image_category_index)
                image_paths = []
                image_category_index = []
                image_bytes = []

            payload = json.dumps({'classifierIds': classifier_ids})
            print (payload)
            finishedUrl = "http://localhost:2000/tensorflow/completedTraining"
            headers = {"Authorization": JWT, 'Content-Type': 'application/json'}
            r = requests.post(finishedUrl, headers=headers, data=payload)


    def start_training(self, classifier_id, image_paths, labels):
        #
        image_bytes = []            # store the byte data of the training images
        for img_path in image_paths:
            data = tf.gfile.FastGFile(img_path, 'rb').read()
            image_bytes.append(data)

        print("Converting to tfrecord...")

        # print(image_category_index)
        convert.convert_to("../../../resources/tfrecord", image_bytes, labels)
        train.train(
            self.checkpoint_directory,
            self.train_directory,
            "../../../resources/tfrecord",
            logo_name=classifier_id) #ask bryce to fix logoname
        self.swap_out_checkpoints(self.train_directory+'/prev',self.train_directory)

def main():
    # Driver().get_training_images()
    Driver().get_classify_images()
    # Driver().start_classify()
    # Driver().start_eval()

if __name__ == "__main__":
    main()
