import config as conf
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras

# Load the data
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    conf.TRAINING_IMAGES_PATH,
    validation_split=conf.TRAIN_VAL_SPLIT,
    subset="training",
    seed=conf.SEED,
    image_size=conf.IMG_SIZE,
    batch_size=conf.BATCH_SIZE,
    shuffle=True,
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    conf.TRAINING_IMAGES_PATH,
    validation_split=conf.TRAIN_VAL_SPLIT,
    subset="validation",
    seed=conf.SEED,
    image_size=conf.IMG_SIZE,
    batch_size=conf.BATCH_SIZE,
    shuffle=True,
)

# Add data augmentation
with tf.device('/cpu:0'):
    data_augmentation = keras.Sequential(
        [
            layers.RandomRotation(0.15),
        ]
    )

train_ds = train_ds.prefetch(buffer_size=conf.BATCH_SIZE)
val_ds = val_ds.prefetch(buffer_size=conf.BATCH_SIZE)
