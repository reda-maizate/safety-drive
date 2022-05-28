import datetime
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import cv2
import os
import json
from tqdm import tqdm
from glob import glob
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import tensorflow as tf
import tensorflow.keras as keras
from keras.utils.tf_utils import set_random_seed
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, GlobalAveragePooling2D


df = pd.read_csv('C:/Users/Bonjour/Etudes&Travail/Projets/PyCharm/DeepLearningSafetyDrive/Data/driver_imgs_list.csv')
print(df.head(5))

# Groupby subjects
by_drivers = df.groupby('subject')
# Group unique drivers
unique_drivers = by_drivers.groups.keys()  # drivers id

print('There are : ', len(unique_drivers), ' unique drivers')
print('There is a mean of ', round(df.groupby('subject').count()['classname'].mean()), ' images by driver.')

num_classes = 10


# Read with opencv
def get_image(path, img_rows, img_cols, color_type=3):
    if color_type == 1:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (img_rows, img_cols))  # Reduce size
    return img


# Loading training dataset
def train_data_load(img_rows=64, img_cols=64, color_type=3):
    train_images = []
    train_labels = []

    # Loop over the training folder
    for classes in tqdm(range(num_classes)):
        print('Loading directory c{}'.format(classes))
        files = glob(
            os.path.join(
                'C:\\Users\\Bonjour\\Etudes&Travail\\Projets\\Pycharm\\DeepLearningSafetyDrive\\Data\\train\\c' + str(
                    classes),
                '*.jpg'))
        for file in files:
            img = get_image(file, img_rows, img_cols, color_type)
            train_images.append(img)
            train_labels.append(classes)
    return train_images, train_labels


def read_and_normalize_train_data(img_rows, img_cols, color_type):
    X, labels = train_data_load(img_rows, img_cols, color_type)
    y = np_utils.to_categorical(labels, 10)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    x_train = np.array(x_train, dtype=np.uint8).reshape(-1, img_rows, img_cols, color_type)
    x_test = np.array(x_test, dtype=np.uint8).reshape(-1, img_rows, img_cols, color_type)

    return x_train, x_test, y_train, y_test


# def create_conv_net_model(unique_token_count, unique_token_count_test):
#     model = keras.models.Sequential()
#     model.add(tf.keras.layers.Input(shape=(300,)))
#     model.add(tf.keras.layers.Embedding(max(unique_token_count, unique_token_count_test), 32))
#
#     # for i in range(3):
#     #     model.add(keras.layers.Conv1D(32 * (i + 1), 3, padding='same', activation=keras.activations.relu))
#     #     model.add(keras.layers.MaxPool1D())
#
#     model.add(keras.layers.Conv1D(32, 3, padding='same', activation=keras.activations.relu))
#     model.add(keras.layers.MaxPool1D())
#     model.add(keras.layers.Conv1D(64, 3, padding='same', activation=keras.activations.relu))
#     model.add(keras.layers.MaxPool1D())
#     model.add(keras.layers.Conv1D(128, 3, padding='same', activation=keras.activations.relu))
#     model.add(keras.layers.MaxPool1D())
#     model.add(keras.layers.Flatten())
#
#     # model.add(keras.layers.Dense(1, kernel_regularizer=keras.regularizers.l2(0.01),
#     #                              bias_regularizer=keras.regularizers.l2(0.01)))
#     model.add(keras.layers.Dense(1))
#     return model


def create_conv_net_model_with_skip_connections():
    input_tensor = keras.layers.Input(shape=(28, 28, 1))

    hidden_tensor = input_tensor

    for i in range(10):
        prev_tensor = hidden_tensor
        hidden_tensor = keras.layers.Conv2D(32, (3, 3), padding='same', activation=keras.activations.relu,
                                            kernel_initializer=keras.initializers.he_normal)(hidden_tensor)
        hidden_tensor = keras.layers.Dropout(0.2)(hidden_tensor)
        if i > 0:
            hidden_tensor = keras.layers.Add()([hidden_tensor, prev_tensor]) / 2.0
        else:
            hidden_tensor = keras.layers.Add()([hidden_tensor, keras.layers.Dense(32)(prev_tensor)]) / 2.0

    hidden_tensor = keras.layers.Flatten()(hidden_tensor)
    output_tensor = keras.layers.Dense(10, activation=keras.activations.softmax,
                                       kernel_regularizer=keras.regularizers.l2(0.01),
                                       bias_regularizer=keras.regularizers.l2(0.01))(hidden_tensor)

    model = keras.models.Model(input_tensor, output_tensor)
    return model


def create_conv_net_model(img_rows, img_cols, color_type):
    model = keras.models.Sequential()

    # CNN1
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_rows, img_cols, color_type)))
    model.add(BatchNormalization())
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization(axis=3))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.3))

    # CNN2
    model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(img_rows, img_cols, color_type)))
    model.add(BatchNormalization())
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization(axis=3))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.3))

    # CNN3
    model.add(Conv2D(128, (3, 3), activation='relu', input_shape=(img_rows, img_cols, color_type)))
    model.add(BatchNormalization())
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization(axis=3))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.3))

    model.add(keras.layers.Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.25))
    model.add(Dense(10, activation='softmax'))

    # model.add(keras.layers.Dense(10, kernel_regularizer=keras.regularizers.l2(0.01),
    #                              bias_regularizer=keras.regularizers.l2(0.01)))
    return model


def run_experiments():
    seeds = [42, 51, 69, 13, 7, 123, 12, 23, 321, 420]

    img_rows = 128
    img_cols = 128
    color_type = 1

    # Loading train images
    x_train, x_test, y_train, y_test = read_and_normalize_train_data(img_rows, img_cols, color_type)

    batch_size = 40
    n_epochs = 50

    for seed_idx, seed in enumerate(seeds):
        print(f"running seed experiment {seed_idx} out of {len(seeds)}")
        set_random_seed(seed)

        run_id = f"cnn/3cnn_32_64_128_neurons_bs40/model_seed_{seed}_{str(datetime.datetime.now())}"
        run_id = run_id.replace(" ", "_").replace(":", "_")

        model = create_conv_net_model(img_rows, img_cols, color_type)

        print(model.summary())

        model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        # model.compile(
        #     optimizer=keras.optimizers.SGD(0.1, momentum=0.9),
        #     loss=tf.keras.losses.mean_squared_error
        # )
        history = model.fit(x_train, y_train,
                            validation_data=(x_test, y_test),
                            epochs=n_epochs, batch_size=batch_size, verbose=1)
        # model.fit(x_train, y_train,
        #           validation_data=(x_test, y_test),
        #           callbacks=[keras.callbacks.TensorBoard(f"./logs/iabd1/{run_id}"),
        #                      keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=20, min_lr=0.001),
        #           epochs=300,
        #           batch_size=512)

        print('History of the training', history.history)

        model.save(f"saved_model/{run_id}.keras")


if __name__ == "__main__":
    run_experiments()
