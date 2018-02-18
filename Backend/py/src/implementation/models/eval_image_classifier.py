# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Generic evaluation script that evaluates a model using a given dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import tensorflow as tf

from datasets import my_dataset
from nets import nets_factory
from preprocessing import preprocessing_factory

slim = tf.contrib.slim

def eval(checkpoint_path,eval_dir,dataset_dir,model_name = "inception_v4",batch_size=100):
  if not dataset_dir:
    raise ValueError('You must supply the dataset directory with --dataset_dir')

  tf.logging.set_verbosity(tf.logging.INFO)
  with tf.Graph().as_default():
    tf_global_step = slim.get_or_create_global_step()

    ######################
    # Select the dataset #
    ######################
    dataset = my_dataset.get_split('validation', dataset_dir)

    ####################
    # Select the model #
    ####################
    network_fn = nets_factory.get_network_fn(
        model_name,
        #num_classes=(dataset.num_classes),
        is_training=False,
        logo_names= ['Patagonia'])
    ##############################################################
    # Create a dataset provider that loads data from the dataset #
    ##############################################################
    provider = slim.dataset_data_provider.DatasetDataProvider(
        dataset,
        shuffle=False,
        common_queue_capacity=2 * batch_size,
        common_queue_min=batch_size)
    [image, label] = provider.get(['image', 'label'])

    #####################################
    # Select the preprocessing function #
    #####################################
    preprocessing_name = model_name
    image_preprocessing_fn = preprocessing_factory.get_preprocessing(
        preprocessing_name,
        is_training=False)

    eval_image_size = network_fn.default_image_size

    image = image_preprocessing_fn(image, eval_image_size, eval_image_size)

    images, labels = tf.train.batch(
        [image, label],
        batch_size=batch_size,
        num_threads=4,
        capacity=5 * batch_size)

    ####################
    # Define the model #
    ####################
    logits, _ = network_fn(images, logo_names= ['Patagonia'])
    variables_to_restore = slim.get_variables_to_restore()

    predictions = tf.argmax(logits['Patagonia'], 1)
    labels = tf.squeeze(labels)

    # Define the metrics:
    names_to_values, names_to_updates = slim.metrics.aggregate_metric_map({
        'Accuracy': slim.metrics.streaming_accuracy(predictions, labels),
        'Recall_5': slim.metrics.streaming_recall_at_k(
            logits['Patagonia'], labels, 5),
    })

    # Print the summaries to screen.
    for name, value in names_to_values.items():
      summary_name = 'eval/%s' % name
      op = tf.summary.scalar(summary_name, value, collections=[])
      op = tf.Print(op, [value], summary_name)
      tf.add_to_collection(tf.GraphKeys.SUMMARIES, op)

    # This ensures that we make a single pass over all of the data.
    num_batches = math.ceil(dataset.num_samples / float(batch_size))

    if tf.gfile.IsDirectory(checkpoint_path):
      checkpoint_path = tf.train.latest_checkpoint(checkpoint_path)

    tf.logging.info('Evaluating %s' % checkpoint_path)

    #print('variables_to_restore: ',variables_to_restore)
    return slim.evaluation.evaluate_once(
        master="",
        checkpoint_path=checkpoint_path,
        logdir=eval_dir,
        num_evals=num_batches,
        eval_op=list(names_to_updates.values()),
        variables_to_restore=variables_to_restore)

def main(_):
    print("eval: ",eval("../../resources/train","../../resources/train","../../resources/tfrecord",model_name = "inception_v4",batch_size=100))
main(None)
