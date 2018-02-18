import numpy as np
import os
import tensorflow as tf
import urllib2

from datasets import my_dataset
from nets import inception
from nets import inception_utils
from preprocessing import inception_preprocessing

train_dir = "Users/bryce/Desktop/logo_detection/BelgaLogos/data"

slim.learning.train(
    train_tensor,
    logdir=FLAGS.train_dir,
    master=FLAGS.master,
    is_chief=(FLAGS.task == 0),
    init_fn=_get_init_fn(),
    summary_op=summary_op,
    number_of_steps=FLAGS.max_number_of_steps,
    log_every_n_steps=FLAGS.log_every_n_steps,
    save_summaries_secs=FLAGS.save_summaries_secs,
    save_interval_secs=FLAGS.save_interval_secs,
    sync_optimizer=optimizer if FLAGS.sync_replicas else None)
