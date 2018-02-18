# Where the training (fine-tuned) checkpoint and logs will be saved to.
TRAIN_DIR=../../train

# Where the dataset is saved to.
DATASET_DIR=../../BelgaLogos/tfrecord

# Run evaluation.
python eval_image_classifier.py \
  --checkpoint_path=${TRAIN_DIR} \
  --eval_dir=${TRAIN_DIR} \
  --dataset_name=my \
  --dataset_split_name=validation \
  --dataset_dir=${DATASET_DIR} \
  --model_name=inception_v4
