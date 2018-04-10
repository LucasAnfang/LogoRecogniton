from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import random
import sys
import numpy as np

from PIL import Image


import tensorflow as tf
import dataset_utils


class ImageReader(object):
  """Helper class that provides TensorFlow image coding utilities."""

  def __init__(self):
    # Initializes function that decodes RGB JPEG data.
    self._decode_jpeg_data = tf.placeholder(dtype=tf.string)
    self._decode_jpeg = tf.image.decode_jpeg(self._decode_jpeg_data, channels=3)

  def read_image_dims(self, sess, image_data):
    image = self.decode_jpeg(sess, image_data)
    return image.shape[0], image.shape[1]

  def decode_jpeg(self, sess, image_data):
    image = sess.run(self._decode_jpeg,
                     feed_dict={self._decode_jpeg_data: image_data})
    assert len(image.shape) == 3
    assert image.shape[2] == 3
    return image

def _int64_feature(value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def image_to_tfexample(image_data, image_format, height, width, class_id):
  return tf.train.Example(features=tf.train.Features(feature={
      'image/encoded': _bytes_feature(image_data),
      'image/format': _bytes_feature(image_format),
      'image/class/label': _int64_feature(class_id),
      'image/height': _int64_feature(height),
      'image/width': _int64_feature(width),
  }))
# images and labels array as input
def write_tfrecord(database_dir,images, labels, name):
  num_examples = len(labels)
  if len(images) != num_examples:
    raise ValueError("Images size %d does not match label size %d." %
                     (len(images), num_examples))

  # filename = os.path.join(database_dir, name)
  filename = os.path.abspath(os.path.join(database_dir, name))
  print('Writing', filename)
  writer = tf.python_io.TFRecordWriter(filename)
  for index in range(num_examples):
    with tf.Graph().as_default():
      image_reader = ImageReader()
      with tf.Session('') as sess:
        width, height = image_reader.read_image_dims(sess, images[index])
        image_raw = images[index]
        example = image_to_tfexample(image_raw, str.encode('jpeg'), height, width, int(labels[index]))
        writer.write(example.SerializeToString())

def convert_to(database_dir,images, labels):
    _NUM_VALIDATION = int(len(labels)*.2+1)
    _RANDOM_SEED = 0
    _NUM_SHARDS = 5 #?
    images = np.array(images)
    labels = np.array(labels)
    c = np.c_[images.reshape(len(images), -1), labels.reshape(len(labels), -1)]
    np.random.shuffle(c)
    images = c[:, :images.size//len(images)].reshape(images.shape)
    labels = c[:, labels.size//len(labels):].reshape(labels.shape)
    training_images = images[_NUM_VALIDATION:]
    validation_images = images[:_NUM_VALIDATION]
    training_labels = labels[_NUM_VALIDATION:]
    validation_labels = labels[:_NUM_VALIDATION]
    print("len of training_images",len(training_images))
    print("len of validation_images",len(validation_images))
    num_per_shard_training = int(len(training_images) / float(_NUM_SHARDS))
    for i in range(_NUM_SHARDS):
        write_tfrecord(database_dir,
        training_images[i*num_per_shard_training:(i+1)*num_per_shard_training],
        training_labels[i*num_per_shard_training:(i+1)*num_per_shard_training],
        'logo_train_%05d-of-%05d.tfrecord' % (i, _NUM_SHARDS))
    num_per_shard_validation = int(math.ceil(len(validation_images) / float(_NUM_SHARDS)))
    for i in range(_NUM_SHARDS):
        write_tfrecord(database_dir,
        validation_images[i*num_per_shard_validation:(i+1)*num_per_shard_validation],
        validation_labels[i*num_per_shard_validation:(i+1)*num_per_shard_validation],
        'logo_validation_%05d-of-%05d.tfrecord' % (i, _NUM_SHARDS))


'''def main():
    images = [x for x in range(200)]
    labels = [x for x in range(200)]
    convert_to("tfrecord",images, labels)
main()'''
