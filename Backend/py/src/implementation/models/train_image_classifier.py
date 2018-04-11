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
"""Generic training script that trains a model using a given dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'.'))
from datasets import my_dataset
from deployment import model_deploy
from nets import nets_factory
from preprocessing import preprocessing_factory

slim = tf.contrib.slim
from tensorflow.python.training import saver as tf_saver

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def _configure_learning_rate(learning_rate_decay_type,num_samples_per_epoch, global_step, batch_size):
  """Configures the learning rate.

  Args:
    num_samples_per_epoch: The number of samples in each epoch of training.
    global_step: The global_step tensor.

  Returns:
    A `Tensor` representing the learning rate.

  Raises:
    ValueError: if
  """
  decay_steps = int(num_samples_per_epoch / batch_size * 2.0)

  if learning_rate_decay_type == 'exponential':
    return tf.train.exponential_decay(0.01,
                                      global_step,
                                      decay_steps,
                                      0.94,
                                      staircase=True,
                                      name='exponential_decay_learning_rate')
  elif learning_rate_decay_type == 'fixed':
    return tf.constant(0.01, name='fixed_learning_rate')
  elif learning_rate_decay_type == 'polynomial':
    return tf.train.polynomial_decay(0.01,
                                     global_step,
                                     decay_steps,
                                     0.0001,
                                     power=1.0,
                                     cycle=False,
                                     name='polynomial_decay_learning_rate')
  else:
    raise ValueError('learning_rate_decay_type [%s] was not recognized',
                     learning_rate_decay_type)


def _configure_optimizer(optimizer):
  """Configures the optimizer used for training.

  Args:
    learning_rate: A scalar or `Tensor` learning rate.

  Returns:
    An instance of an optimizer.

  Raises:
    ValueError: if optimizer is not recognized.
  """
  if optimizer == 'adadelta':
    optimizer = tf.train.AdadeltaOptimizer(
        0.01,
        rho=0.95,
        epsilon=1.0)
  elif optimizer == 'adagrad':
    optimizer = tf.train.AdagradOptimizer(
        0.01,
        initial_accumulator_value=0.1)
  elif optimizer == 'adam':
    optimizer = tf.train.AdamOptimizer(
        0.01,
        beta1=0.9,
        beta2=0.999,
        epsilon=1.0)
  elif optimizer == 'ftrl':
    optimizer = tf.train.FtrlOptimizer(
        0.01,
        learning_rate_power=-0.5,
        initial_accumulator_value=0.1,
        l1_regularization_strength=0.0,
        l2_regularization_strength=0.0)
  elif optimizer == 'momentum':
    optimizer = tf.train.MomentumOptimizer(
        0.01,
        momentum=0.9,
        name='Momentum')
  elif optimizer == 'rmsprop':
    optimizer = tf.train.RMSPropOptimizer(
        0.01,
        decay=0.9,
        momentum=0.9,
        epsilon=1.0)
  elif optimizer == 'sgd':
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
  else:
    raise ValueError('Optimizer [%s] was not recognized', optimizer)
  return optimizer

def _get_init_fn(checkpoint_path,train_dir,checkpoint_exclude_scopes = []):
  """Returns a function run by the chief worker to warm-start the training.

  Note that the init_fn is only run when initializing the model during the very
  first global step.

  Returns:
    An init function run by the supervisor.
  """
  if checkpoint_path is None:
    return None

  # Warn the user if a checkpoint exists in the train_dir. Then we'll be
  # ignoring the checkpoint anyway.
  if tf.train.latest_checkpoint(train_dir):
    tf.logging.info(
        'Ignoring --checkpoint_path because a checkpoint already exists in %s'
        % train_dir)
    print("BEFORE checkpoint_path: ",checkpoint_path)
    checkpoint_path = tf.train.latest_checkpoint(train_dir)
    print("AFTER checkpoint_path: ",checkpoint_path)

  exclusions = []
  if checkpoint_exclude_scopes != []:
    exclusions = [scope.strip()
                  for scope in checkpoint_exclude_scopes]

  # TODO(sguada) variables.filter_variables()
  variables_to_restore = []
  for var in slim.get_model_variables():
    # print ("var????: ", var);
    excluded = False
    for exclusion in exclusions:
      if var.op.name.startswith(exclusion):
        excluded = True
        break
    if not excluded:
      variables_to_restore.append(var)

  if tf.gfile.IsDirectory(checkpoint_path):
      checkpoint_path = tf.train.latest_checkpoint(checkpoint_path)
      print("1", checkpoint_path)
  else:
      checkpoint_path = checkpoint_path
      print("2", checkpoint_path)

  tf.logging.info('Fine-tuning from %s' % checkpoint_path)

  return slim.assign_from_checkpoint_fn(
      checkpoint_path,
      variables_to_restore,
      ignore_missing_vars=True)


def _get_variables_to_train(trainable_scopes):
  """Returns a list of variables to train.

  Returns:
    A list of variables to train by the optimizer.
  """
  if trainable_scopes is []:
    return tf.trainable_variables()
  else:
    scopes = [scope.strip() for scope in trainable_scopes]

  variables_to_train = []
  for scope in scopes:
    variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope)
    variables_to_train.extend(variables)
  return variables_to_train


def train(checkpoint_path,train_dir,dataset_dir,
         model_name = "inception_v4",logo_name="",checkpoint_exclude_scopes =[],
          optimizer="rmsprop",learning_rate_decay_type='fixed',batch_size=32,weight_decay=0.00004,
          max_number_of_steps=400,log_every_n_steps=100,save_summaries_secs=60,save_interval_secs=60,task_id=0):


  trainable_scopes =['InceptionV4/Logits/'+logo_name+'_Logits','InceptionV4/Logits/'+logo_name+'_AuxLogits']

  if not dataset_dir:
    raise ValueError('You must supply the dataset directory with --dataset_dir')

  tf.logging.set_verbosity(tf.logging.INFO)
  with tf.Graph().as_default():
    #######################
    # Config model_deploy #
    #######################
    deploy_config = model_deploy.DeploymentConfig(
        num_clones=1,
        clone_on_cpu=False,
        replica_id=task_id,
        num_replicas=1,
        num_ps_tasks=0)

    # Create global_step
    with tf.device(deploy_config.variables_device()):
      global_step = slim.create_global_step()

    ######################
    # Select the dataset #
    ######################
    dataset = my_dataset.get_split('train', dataset_dir)

    ######################
    # Select the network #
    ######################
    network_fn = nets_factory.get_network_fn(
        model_name,
        #num_classes=(dataset.num_classes),
        weight_decay=weight_decay,
        is_training=True,
        logo_names= [logo_name])

    #####################################
    # Select the preprocessing function #
    #####################################
    preprocessing_name =  model_name
    image_preprocessing_fn = preprocessing_factory.get_preprocessing(
        preprocessing_name,
        is_training=True)

    ##############################################################
    # Create a dataset provider that loads data from the dataset #
    ##############################################################
    with tf.device(deploy_config.inputs_device()):
      provider = slim.dataset_data_provider.DatasetDataProvider(
          dataset,
          num_readers=4,
          common_queue_capacity=20 * batch_size,
          common_queue_min=10 * batch_size)
      [image, label] = provider.get(['image', 'label'])

      train_image_size = network_fn.default_image_size

      image = image_preprocessing_fn(image, train_image_size, train_image_size)

      images, labels = tf.train.batch(
          [image, label],
          batch_size=batch_size,
          num_threads=4,
          capacity=5 * batch_size)
      labels = slim.one_hot_encoding(
          labels, dataset.num_classes)
      batch_queue = slim.prefetch_queue.prefetch_queue(
          [images, labels], capacity=2 * deploy_config.num_clones)

    ####################
    # Define the model #
    ####################
    def clone_fn(batch_queue,optimizer,batch_size,learning_rate_decay_type,logo_name=""):
      """Allows data parallelism by creating multiple clones of network_fn."""
      print("BEGIN")
      with tf.device(deploy_config.inputs_device()):
        images, labels = batch_queue.dequeue()
      print("BEGIN")
      logits, end_points = network_fn(images, logo_names= [logo_name])
      print("END")
      print("logo_name_is: ",logo_name)
      #############################
      # Specify the loss function #
      #############################
      if logo_name != "":
          logo_name += "_"
      if logo_name+'AuxLogits' in end_points:
        tf.losses.softmax_cross_entropy(
            logits=end_points[logo_name+'AuxLogits'], onehot_labels=labels,
            label_smoothing=0.0, weights=0.4, scope='aux_loss')
        tf.losses.softmax_cross_entropy(
              logits=end_points[logo_name+'Logits'], onehot_labels=labels,
              label_smoothing=0.0, weights=1.0)
      return end_points

    # Gather initial summaries.
    summaries = set(tf.get_collection(tf.GraphKeys.SUMMARIES))

    clones = model_deploy.create_clones(deploy_config, lambda batch_queue,optimizer,batch_size,learning_rate_decay_type: clone_fn(batch_queue,optimizer,batch_size,learning_rate_decay_type,logo_name=logo_name), [batch_queue,optimizer,batch_size,learning_rate_decay_type])
    first_clone_scope = deploy_config.clone_scope(0)
    # Gather update_ops from the first clone. These contain, for example,
    # the updates for the batch_norm variables created by network_fn.
    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS, first_clone_scope)

    # Add summaries for end_points.
    end_points = clones[0].outputs
    for end_point in end_points:
      x = end_points[end_point]
      summaries.add(tf.summary.histogram('activations/' + end_point, x))
      summaries.add(tf.summary.scalar('sparsity/' + end_point,
                                      tf.nn.zero_fraction(x)))

    # Add summaries for losses.
    for loss in tf.get_collection(tf.GraphKeys.LOSSES, first_clone_scope):
      summaries.add(tf.summary.scalar('losses/%s' % loss.op.name, loss))

    # Add summaries for variables.
    for variable in slim.get_model_variables():
      summaries.add(tf.summary.histogram(variable.op.name, variable))

    #########################################
    # Configure the optimization procedure. #
    #########################################
    with tf.device(deploy_config.optimizer_device()):
      learning_rate = _configure_learning_rate(learning_rate_decay_type,dataset.num_samples, global_step,batch_size)
      optimizer = _configure_optimizer(optimizer=optimizer)
      summaries.add(tf.summary.scalar('learning_rate', learning_rate))


    # Variables to train.
    variables_to_train = _get_variables_to_train(trainable_scopes)

    #  and returns a train_tensor and summary_op
    total_loss, clones_gradients = model_deploy.optimize_clones(
        clones,
        optimizer,
        var_list=variables_to_train)
    # Add total_loss to summary.
    summaries.add(tf.summary.scalar('total_loss', total_loss))

    # Create gradient updates.
    grad_updates = optimizer.apply_gradients(clones_gradients,
                                             global_step=global_step)
    update_ops.append(grad_updates)

    update_op = tf.group(*update_ops)
    with tf.control_dependencies([update_op]):
      train_tensor = tf.identity(total_loss, name='train_op')

    # Add the summaries from the first clone. These contain the summaries
    # created by model_fn and either optimize_clones() or _gather_clone_loss().
    summaries |= set(tf.get_collection(tf.GraphKeys.SUMMARIES,
                                       first_clone_scope))

    # Merge all summaries together.
    summary_op = tf.summary.merge(list(summaries), name='summary_op')

    ###########################
    # Kicks off the training. #
    ###########################
    # sess = tf.Session()
    # arg_scope = inception_v4_arg_scope()
    # input_tensor = tf.placeholder(tf.float32, (None, 299, 299, 3))
    # with slim.arg_scope(arg_scope):
    #     logits, end_points = inception_v4(input_tensor, is_training=False)
    # saver = tf.train.Saver()
    # saver.restore(sess, checkpoint_file)

    slim.learning.train(
        train_tensor,
        logdir=train_dir,
        master="",
        is_chief=(task_id == 0),
        init_fn=_get_init_fn(checkpoint_path,train_dir+'/prev',checkpoint_exclude_scopes),
        summary_op=summary_op,
        number_of_steps=max_number_of_steps,
        log_every_n_steps=log_every_n_steps,
        save_summaries_secs=save_summaries_secs,
        save_interval_secs=save_interval_secs)



'''def main(_):
     train("../../resources/checkpoints/inception_v4.ckpt","../../resources/train","../../resources/tfrecord", logo_name="Nike")
main(None)'''
