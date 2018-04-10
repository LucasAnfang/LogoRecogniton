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
config.read('../config.ini')

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
#
#
#
# '''
# TODO:
# AS YOU REMOVE MODULES DOWN BELOW, LOOK UP AT THE IMPORTS AND REMOVE THEM
#
# Post entities (list of dictionaries) comes up a lot
# The idea was keeping all the dataset entities in one object
# That object includes the image binaries, path, and post metadata (caption, hashtags, user, etc.)
#
# You should find a point in your workflow to stitch the results from this with the rest of the
# information associated with a post you are classifying the image of
# '''
# class Driver:
#     def __init__(self):
#         # TODO: This now stored on your rest API so ignore this and make calls to routes to grab and store checkpoints
#         self.checkpoint_directory = "../../../resources/checkpoints"
#         # if it has been tested
#         self.testvar = False
#
#     # def load_image(self,addr):
#     #     # read an image and resize to (600, 600)
#     #     # cv2 load images as BGR, convert it to RGB
#     #     img = cv2.imread(addr)
#     #     img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_CUBIC)
#     #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     #     img = img.astype(np.float32)
#     #     return img
#
#     def download_checkpoints(self):
#         # TODO: This now using your rest api
#         return self.checkpoint_controller.download_checkpoints(destination_directory = self.checkpoint_directory+'/prev')
#
#     def upload_checkpoints(self):
#         # TODO: This now using your rest api
#         self.checkpoint_controller.upload_checkpoints(self.checkpoint_directory+'/prev')
    # def start_eval(self):
    #     # train.train("../../../resources/checkpoints/inception_v4.ckpt", self.checkpoint_directory,"../../../resources/tfrecord", logo_name=brand) #ask bryce to fix logoname
    #     eval = eval.eval("../../../resources/train","../../../resources/train","../../../resources/tfrecord",model_name = "inception_v4",batch_size=100)
    #     print("eval: ", eval)
    #
    # def start_processing(self):
    #     print("starting driver...")
    #
    #
    #     # headers = {"Authorization": self.auth['JWT']}
    #     JWT = "BEARER eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlbnNvcmZsb3dAbG9nb2RldGVjdC5jb20iLCJ1c2VySWQiOiI1YWM0MTE3YTMzZDA5ODJmOGM0ZWEyNjkiLCJpYXQiOjE1MjI3OTg5ODYsImV4cCI6MTU1NDM1NjU4Nn0.y25h7mA6NWUpCq7EeecZ3FuP6IUJpougNVrl695SyAU"
    #     headers = {"Authorization": JWT}
    #     # res = requests.get(self.routes['Training'], headers=headers)
    #     res = requests.get("http://localhost:2000/tensorflow/training", headers=headers)
    #
    #     if res.status_code == requests.codes.ok:
    #         print("Retrieved training images from Rest API")
    #
    #         # stores the names of all training images
    #         image_paths = []
    #         # store the name of each category, and associate it with the index of the array
    #         category_names = {}
    #         # store the (index of) each training image's category
    #         # use the category_names array to map the category name to the index
    #         image_category_index = []
    #
    #         label_index = 0
    #         image_index = 0
    #         image_bytes = []
    #
    #
    #         # for each node in a classifier, get the training data
    #         classifiers = res.json()['classifiers']
    #         for i in range (len(classifiers)):
    #             # print ("Classifier", i, classifiers[i]['name'])
    #             nodes = classifiers[i]['nodes']
    #             for j in range (len(nodes)):
    #                 # print ("Node", j, nodes[j]['name'])
    #                 category_names[label_index] = nodes[j]['name'];
    #                 trainingData = nodes[j]['trainingData']
    #                 for k in range (len(trainingData)):
    #                     # download training images from REST API
    #                     # print (trainingData[k], '->', fname)
    #                     fname = '../../../storage/train/'+ str(image_index) +'.jpg'
    #                     image_index += 1
    #                     # print (trainingData[k], '->', fname)
    #
    #                     response = requests.get(trainingData[k], stream=True)
    #
    #                     with open(fname, 'wb') as out_file:
    #                         shutil.copyfileobj(response.raw, out_file)
    #
    #                     image_paths.append(fname)
    #                     image_category_index.append(j)
    #                 label_index += 1
    #         print("Converting to tfrecord")
    #
    #
    #         for img_path in image_paths:
    #             data = tf.gfile.FastGFile(img_path, 'rb').read()
    #             image_bytes.append(data)
    #
    #
    #         print(image_category_index)
    #         convert.convert_to("../../../resources/tfrecord", image_bytes, image_category_index)
    #         print("training")
    #         brand = "Nike"
    #         train.train("../../../resources/checkpoints/inception_v4.ckpt", self.checkpoint_directory,"../../../resources/tfrecord", logo_name=brand) #ask bryce to fix logoname

        # self.brand_names = self.retrieve_supported_brands()

        # self.download_checkpoints()
        # for brand in self.brand_names:
        #     self.testvar = False
        #     training_post_entities_blobs = self.retrieve_unproccessed_training_post_entities(brand)
        #     if(len(training_post_entities_blobs) != 0):
        #          training_post_entities_list = self.extract_post_entities_data(training_post_entities_blobs, isTraining = True)
        #         # dataset is training_post_entities_list
        #          self.process_training_post_entries(brand, training_post_entities_list)
        #     else:
        #          print("No training data to be processed")
        #     operational_post_entities_blobs = self.retrieve_unproccessed_operational_post_entities(brand)
        #     if(len(operational_post_entities_blobs) != 0):
        #         operational_post_entities_list = self.extract_post_entities_data(operational_post_entities_blobs, isOperational = True)
        #         self.process_operational_post_entries(brand, operational_post_entities_list)
        #     else:
        #         print("No operational data to be processed")
        #     # self.update_log_files(training_post_entities_blobs, operational_post_entities_blobs)
        # self.upload_checkpoints()

    # def process_operational_post_entries(self, brand, post_entities_list):
    #     nameMap = []
    #     with open("../../models/class_list.txt", "r") as ins:
    #         for line in ins:
    #             nameMap.append(line.split('\n')[0])
    #     for post_entities in post_entities_list:
    #         image_paths = [post_entity['image_path'] for post_entity in post_entities.posts]
    #         batch_size = 30
    #         r2d2 = R2D2(self.input_controller)
    #         r2d2.set_image_paths(image_paths, batch_size = batch_size)
    #         current_index = 0
    #         #node_lookup = image_utils.NodeLookup()
    #         #brand = [x.capitalize() for x in brand]
    #         while(True):
    #             indices = [(current_index + i) for i in range(batch_size)]
    #             images = [r2d2.get_image_with_path(post_entities.posts[i]['image_path']) for i in indices if (i < len(post_entities.posts))]
    #             current_index += len(images)
    #             if(len(images) == 0):
    #                 break
    #             print ("testvar: ", self.testvar)
    #             results = test.classify(self.checkpoint_directory+'/prev',images,logo_names=["",brand],reuse=self.testvar)
    #             self.testvar = True
    #             patching_index = indices[0]
    #             for index in range(len(images)):
    #                 post_entities.setImageContextAtIndex(patching_index, [nameMap[node_id-1] for node_id in results[""][index]])
    #                 post_entities.setAccuracyAtIndex(patching_index, float(results[brand][index][1]))
    #                 post_entities.setHasLogoAtIndex(patching_index, bool(round(results[brand][index][1])))
    #                 patching_index += 1
    #         self.table_manager.upload_instagram_post_entities(brand, post_entities)
    #     print("Classification completed for brand: ", brand)

    # def process_training_post_entries(self, brand, post_entities_list):
    #     for post_entities in post_entities_list:
    #
    #         no_logo_post_entities = [post_entity for post_entity in post_entities.posts if post_entity['has_logo'] == False]
    #         logo_post_entities = [post_entity for post_entity in post_entities.posts if post_entity['has_logo'] == True]
    #
    #         no_logo_image_paths = [post_entity['image_path'] for post_entity in no_logo_post_entities]
    #         logo_image_paths = [post_entity['image_path'] for post_entity in logo_post_entities]
    #
    #         no_logo_r2d2 = R2D2(self.input_controller)
    #         logo_r2d2 = R2D2(self.input_controller)
    #
    #         no_logo_r2d2.set_image_paths(no_logo_image_paths)
    #         logo_r2d2.set_image_paths(logo_image_paths)
    #
    #         no_logo_images = []
    #         logo_images = []
    #
    #         convert.convert_to("../../../resources/tfrecord",images,labels)
    #         train.train("../../../resources/checkpoints/inception_v4.ckpt", self.checkpoint_directory,"../../../resources/tfrecord", logo_name=brand) #ask bryce to fix logoname
    #         self.checkpoint_controller.swap_out_checkpoints(self.checkpoint_directory+'/prev',self.checkpoint_directory)
    #     print("Training completed for brand: ", brand)

#     def retrieve_supported_brands(self):
#         return self.input_controller.get_container_directories()
#
#     def extract_post_entities_data(self, post_entities_blobs, isTraining = False, isOperational = False):
#         if(isTraining == isOperational):
#             raise ValueError('IG post entities has to be either training or operational (not both)')
#         post_entities_list = []
#         for post_entities in post_entities_blobs:
#             brand_name = post_entities.name.split('/')[0]
#             ipe = InstagramPostEntities(isTraining = isTraining, isClassification = isOperational)
#             ipe.deserialize(post_entities.content)
#             print("extracting ipe data for brand", brand_name, "from resource", post_entities.name)
#             post_entities_list.append(ipe)
#         return post_entities_list
#
#     # TODO: These two will be gone because your Rest API will only return docs of unprocessed datasets using mongo find features
#     def retrieve_unproccessed_training_post_entities(self, brand_name):
#         return self.input_controller.download_brand_training_post_entities(brand_name, isProcessed = False)
#
#     def retrieve_unproccessed_operational_post_entities(self, brand_name):
#         return self.input_controller.download_brand_operational_post_entities(brand_name, isProcessed = False)
#
# '''
#     The idea of R2D2 was giving it a list of image paths,
#     batch download the calls efficiently and only load images when they are imediatly wanted for processing
#     I will make a copy of R2D2 below this to show what it should be for you
# '''
# class R2D2:
#     # def __init__(self)
#     # def __init__(self, input_controller):
#     #     self.input_controller = input_controller
#
#     def reset(self):
#         self.current_index = 0
#         self.cache = []
#
#     def set_image_paths(self, image_paths, batch_size = 10):
#         self.image_paths = image_paths
#         self.batch_size = batch_size
#         self.reset()
#         self.batch_download()
#
#     def is_cache_empty(self):
#         return (len(self.cache) == 0)
#
#     def get_image_with_path(self, full_blob_name):
#         if(self.is_cache_empty() == True):
#             self.batch_download()
#         return self.get_blob_from_cache(full_blob_name)
#
#     def get_blob_from_cache(self, full_blob_name):
#         blob = None
#         for index in range(len(self.cache)):
#             if(self.cache[index].name == full_blob_name):
#                 print( "blob with path: " + full_blob_name + " found in cache")
#                 blob = self.cache[index].content
#                 self.cache.pop(index)
#                 break
#         if(blob == None):
#             blob = self.download_data(full_blob_name)
#             print( "blob with path: " + full_blob_name + " NOT found in cache")
#         return blob
#
#     def download_data(self, full_blob_name):
#         return self.input_controller.download_data(full_blob_name)
#
#     def batch_download(self):
#         if(self.is_cache_empty() == False):
#             return
#         indices = [(self.current_index + i) for i in range(self.batch_size)]
#         paths = [self.image_paths[i] for i in indices if (i < len(self.image_paths))]
#         print ("downloading next batch to cache...")
#         self.current_index += len(paths)
#         # if(len(paths) != 0):
#             # self.cache.extend(self.input_controller.parallel_download(paths))
#
# # TODO: Fix The class below to fit yours while looking at the one above (test it in a seperate file)
# # Look at this https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
# class C3PO:
#     def __init__(self, mode = 'image_download'):
#         if(mode == 'image_download'):
#             self.image_download_enabled = True
#
#     def reset(self):
#         self.current_index = 0
#         self.cache = []
#
#     def set_urls(self, urls, batch_size = 10):
#         self.urls = urls
#         self.batch_size = batch_size
#         self.reset()
#         self.batch_download()
#
#     def is_cache_empty(self):
#         return (len(self.cache) == 0)
#
#     def get_artifact_with_url(self, url):
#         if(self.is_cache_empty() == True):
#             self.batch_download()
#         return self.get_artifact_from_cache(url)
#
#     def get_artifact_from_cache(self, url):
#         blob = None
#         for index in range(len(self.cache)):
#             if(self.cache[index].name == full_blob_name):
#                 print ("blob with path: " + full_blob_name + " found in cache")
#                 blob = self.cache[index].content
#                 self.cache.pop(index)
#                 break
#         if(blob == None):
#             blob = self.download_data(full_blob_name)
#             print( "blob with path: " + full_blob_name + " NOT found in cache")
#         return blob
#
#     def download_data(self, full_blob_name):
#         return self.input_controller.download_data(full_blob_name)
#
#     def batch_download(self):
#         if(self.is_cache_empty() == False):
#             return
#         indices = [(self.current_index + i) for i in range(self.batch_size)]
#         paths = [self.image_paths[i] for i in indices if (i < len(self.image_paths))]
#         print ("downloading next batch to cache...")
#         self.current_index += len(paths)
#         if(len(paths) != 0):
#             self.cache.extend(self.parallel_download(paths))
#
#     def parallel_download(self, urls):
#         if(full_blob_names == None):
#             return None
#         threads = []
#         results = []
#         for full_blob_name in full_blob_names:
#             result = {'blob': None}
#             t = threading.Thread(target=self._download_blob_helper, args=(container_name,full_blob_name, result))
#             results.append(result)
#             threads.append(t)
#             t.start()
#         [t.join() for t in threads]
#         blobs = [result['blob'] for result in results if result['blob'] != None]
#         return blobs
#
#     def _download_blob_helper(self, container_name, full_blob_name, result):
#         if(self.exists(container_name, full_blob_name)):
#             result['blob'] = self.download_data(container_name, full_blob_name)
#         else:
#             return None



'''
TODO:
AS YOU REMOVE MODULES DOWN BELOW, LOOK UP AT THE IMPORTS AND REMOVE THEM

Post entities (list of dictionaries) comes up a lot
The idea was keeping all the dataset entities in one object
That object includes the image binaries, path, and post metadata (caption, hashtags, user, etc.)

You should find a point in your workflow to stitch the results from this with the rest of the
information associated with a post you are classifying the image of
'''
class Driver:
    def __init__(self):
        # TODO: This now stored on your rest API so ignore this and make calls to routes to grab and store checkpoints
        self.checkpoint_directory = "../../../resources/checkpoints"
        # if it has been tested
        self.testvar = False

    # def load_image(self,addr):
    #     # read an image and resize to (600, 600)
    #     # cv2 load images as BGR, convert it to RGB
    #     img = cv2.imread(addr)
    #     img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_CUBIC)
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     img = img.astype(np.float32)
    #     return img

    def download_checkpoints(self):
        # TODO: This now using your rest api
        return self.checkpoint_controller.download_checkpoints(destination_directory = self.checkpoint_directory+'/prev')

    def upload_checkpoints(self):
        # TODO: This now using your rest api
        self.checkpoint_controller.upload_checkpoints(self.checkpoint_directory+'/prev')

    def start_eval(self):
        # train.train("../../../resources/checkpoints/inception_v4.ckpt", self.checkpoint_directory,"../../../resources/tfrecord", logo_name=brand) #ask bryce to fix logoname
        eval = eval.eval("../../../resources/train","../../../resources/train","../../../resources/tfrecord",model_name = "inception_v4",batch_size=100)
        print("eval: ", eval)

    def start_processing(self):
        print("starting driver...")


        # headers = {"Authorization": self.auth['JWT']}
        JWT = "BEARER eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlbnNvcmZsb3dAbG9nb2RldGVjdC5jb20iLCJ1c2VySWQiOiI1YWM0MTE3YTMzZDA5ODJmOGM0ZWEyNjkiLCJpYXQiOjE1MjI3OTg5ODYsImV4cCI6MTU1NDM1NjU4Nn0.y25h7mA6NWUpCq7EeecZ3FuP6IUJpougNVrl695SyAU"
        headers = {"Authorization": JWT}
        # res = requests.get(self.routes['Training'], headers=headers)
        res = requests.get("http://localhost:2000/tensorflow/training", headers=headers)

        if res.status_code == requests.codes.ok:
            print("Retrieved training images from Rest API")

            # stores the names of all training images
            image_paths = []
            # store the name of each category, and associate it with the index of the array
            category_names = {}
            # store the (index of) each training image's category
            # use the category_names array to map the category name to the index
            image_category_index = []

            label_index = 0
            image_index = 0
            image_bytes = []


            # for each node in a classifier, get the training data
            classifiers = res.json()['classifiers']
            for i in range (len(classifiers)):
                # print ("Classifier", i, classifiers[i]['name'])
                nodes = classifiers[i]['nodes']
                for j in range (len(nodes)):
                    # print ("Node", j, nodes[j]['name'])
                    category_names[label_index] = nodes[j]['name'];
                    trainingData = nodes[j]['trainingData']
                    for k in range (len(trainingData)):
                        # download training images from REST API
                        # print (trainingData[k], '->', fname)
                        fname = '../../../storage/train/'+ str(image_index) +'.jpg'
                        image_index += 1
                        # print (trainingData[k], '->', fname)

                        response = requests.get(trainingData[k], stream=True)

                        with open(fname, 'wb') as out_file:
                            shutil.copyfileobj(response.raw, out_file)

                        image_paths.append(fname)
                        image_category_index.append(j)
                    label_index += 1
            print("Converting to tfrecord")


            for img_path in image_paths:
                data = tf.gfile.FastGFile(img_path, 'rb').read()
                image_bytes.append(data)


            print(image_category_index)
            convert.convert_to("../../../resources/tfrecord", image_bytes, image_category_index)
            print("training")
            brand = "Nike"
            train.train("../../../resources/checkpoints/inception_v4.ckpt", self.checkpoint_directory,"../../../resources/tfrecord", logo_name=brand) #ask bryce to fix logoname


def main():
    Driver().start_processing()
    # Driver().start_eval()
    # Driver().start_eval()

if __name__ == "__main__":
    main()
