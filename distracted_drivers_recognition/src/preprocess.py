import tensorflow as tf
from tensorflow.keras import layers  # pylint: disable=import-error
from tensorflow import keras
import distracted_drivers_recognition.src.config as conf

# from distracted_drivers_recognition.src.utils import show_images


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
with tf.device("/cpu:0"):
    data_augmentation = keras.Sequential(
        [
            layers.RandomRotation(0.15),
        ]
    )

train_ds = train_ds.prefetch(buffer_size=conf.BATCH_SIZE)
val_ds = val_ds.prefetch(buffer_size=conf.BATCH_SIZE)

# show_images(train_ds)
