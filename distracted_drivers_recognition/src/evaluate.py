import os
import random
import config as conf
import utils
import tensorflow as tf
from tensorflow import keras

# Use a trained model
model = keras.models.load_model(os.path.join(conf.OUTPUT_PATH, "base_model_ep_10_val_acc_0.82.h5"))
# keras.utils.plot_model(model, "model.png", show_shapes=True)

# Evaluate the model
test_files = os.listdir(conf.TEST_IMAGES_PATH)
random_img = random.choice(test_files)

img = keras.preprocessing.image.load_img(
    os.path.join(conf.TEST_IMAGES_PATH, random_img), target_size=conf.IMG_SIZE
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create batch axis

predictions = model.predict(img_array)

# Show the random image and the predictions
utils.show_image(img_array, predictions[0])
