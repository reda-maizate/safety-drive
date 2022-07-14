import os
import random
import tensorflow as tf
from tensorflow import keras
from distracted_drivers_recognition.src import config as conf, utils
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from distracted_drivers_recognition.src.preprocess import val_ds
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Use a trained model
    model = keras.models.load_model(
        os.path.join(conf.OUTPUT_PATH, "base_model_ep_39_val_acc_0.98.h5")
    )
    # keras.utils.plot_model(model, "model.png", show_shapes=True)

    y_vals = []
    y_preds = []

    for i in val_ds.as_numpy_iterator():
        y_vals.extend(i[1])
        preds = model.predict(i[0])
        for y in preds:
            y_preds.append(np.argmax(y))

    matrix = confusion_matrix(y_vals, y_preds)
    m = pd.DataFrame(matrix)
    m.style.background_gradient(cmap="coolwarm")
    plt.show()
    cl = classification_report(y_vals, y_preds)
    print(matrix)
    print(cl)

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
