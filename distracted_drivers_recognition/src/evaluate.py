import os
import random
import tensorflow as tf
from tensorflow import keras
from distracted_drivers_recognition.src import config as conf, utils


if __name__ == "__main__":
    # Use a trained model
    model = keras.models.load_model(
        os.path.join(conf.OUTPUT_PATH, "base_model_ep_39_val_acc_0.98.h5")
    )
    # keras.utils.plot_model(model, "model.png", show_shapes=True)

    # Evaluate the model
    test_files = os.listdir(conf.TEST_IMAGES_PATH)
    random_imgs = random.sample(test_files, k=9)

    imgs = []
    preds = []
    for random_img in random_imgs:
        img = keras.preprocessing.image.load_img(
            os.path.join(conf.TEST_IMAGES_PATH, random_img), target_size=conf.IMG_SIZE
        )
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis
        imgs.append(img_array)

        predictions = model.predict(img_array)[0]
        preds.append(predictions)

    # Show the random image and the predictions
    utils.show_images_with_labels(imgs, preds)
