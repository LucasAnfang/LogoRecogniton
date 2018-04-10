import numpy as np
import os
import tensorflow as tf
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import image_utils

from datasets import my_dataset
from nets import inception
from nets import inception_utils
from preprocessing import inception_preprocessing
from operator import add
slim = tf.contrib.slim

def classify(checkpoints_dir, images,logo_names=[""], reuse=False):
    image_size = inception.inception_v4.default_image_size
    probabilities_list = []
    processed_image_list = []
    images_list = []
    output_probabilities = []
    for image in images:
        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.resize_image_with_crop_or_pad(image, 600, 600)
        processed_image = inception_preprocessing.preprocess_image(image,
                                                             image_size,
                                                             image_size,
                                                             is_training=False)
        #processed_images  = tf.expand_dims(processed_image, 0)
        images_list.append(image)
        processed_image_list.append(processed_image)
    with slim.arg_scope(inception_utils.inception_arg_scope()):
        logits, _ = inception.inception_v4(processed_image_list,
                               #num_classes=2,
                               reuse=reuse,
                               is_training=False,
                               logo_names= logo_names)
        probabilities = []
        output_probabilities = []
        for logo_name in logo_names:
            probabilities.append(tf.nn.softmax(logits[logo_name]))

        if tf.gfile.IsDirectory(checkpoints_dir):
          checkpoints_dir = tf.train.latest_checkpoint(checkpoints_dir)

        init_fn = slim.assign_from_checkpoint_fn(
        checkpoints_dir,
        slim.get_model_variables('InceptionV4'),
        ignore_missing_vars=True)
        with tf.Session() as sess:
            init_fn(sess)
            output_probabilities  = sess.run([images_list,
                                             processed_image_list]
                                             + probabilities)[2:]
        output_dict = {}
        print("range(len(output_probabilities): ", range(len(output_probabilities)))
        for index in range(len(output_probabilities)):
            print( 'logo_names[index]:[{}]'.format(logo_names[index]))
            print('type logo_names[index]',type(logo_names[index]));
            if logo_names[index] == "":
                print("here???????????????????")
                output_dict [logo_names[index]] = output_probabilities[index]
            else:
                output_dict [logo_names[index]] = output_probabilities[index]
            print ("output_dict [""]: ", output_dict [""].shape)

        print ("final 0,780 prob output_dict [""]: ", output_dict[""][0][780]);
        output_dict[""] = np.argsort(output_dict[""], axis=1)[:, ::-1][:, :5]
        # print ("final output_dict [""]: ", output_dict [""])
        return output_dict

def setup_then_classify(input_folder):
    images = []
    nameMap = []
    indexMap = []
    classMap = {}
    with open("../../models/class_list.txt", "r") as ins:
        for line in ins:
            nameMap.append(line.split('\n')[0])
    with open("../../models/imagenet_lsvrc_2015_synsets.txt", "r") as ins:
        index = 0
        for line in ins:
            indexMap.append(line.split('\n')[0])
    with open("../../models/imagenet_metadata.txt", "r") as ins:
        for line in ins:
            word = line.split()
            classMap[word[0]] = word[1]
    #node_lookup = image_utils.NodeLookup()
    for filename in os.listdir(input_folder):
        image = os.path.join(input_folder, filename)
        print ("filename:", image)

        images.append(tf.read_file(image))
    results = classify("../../../resources/checkpoints/inception_v4.ckpt",images,logo_names=[""])
    for index in range(len(image)):
            print (np.shape(results[""][index]))
            print ("setup: ",results[""][index][0]-1,"is ->",nameMap[results[""][index][0]-1])
            a = [ nameMap[node_id-1] for node_id in results[""][index]]
            print('class for image ', index,': ', a)
# main(None)
