import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from keras.models import Model
from keras.layers import Dense, Dropout, Add, Input, BatchNormalization, Activation
from keras.layers import  Conv2D, AveragePooling2D, Flatten
import cv2
import glob
import os

img_rows = 224
img_cols = 224

df = pd.read_csv("C:/Users/Bonjour/Etudes&Travail/Projets/PyCharm/DeepLearningSafetyDrive/Data/driver_imgs_list.csv")

df.head()

def load_image(path, rows=None, cols=None, gray=True):
    if gray:
        img = cv2.imread(path,0)
    else:
        img = cv2.imread(path)
    if rows != None and cols != None:
        img = cv2.resize(img,(rows,cols))
    return img

from tqdm import tqdm
from keras.utils import np_utils
from glob import glob

# Read with opencv
def get_image(path, img_rows, img_cols, color_type=3):
    if color_type == 1:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (img_rows, img_cols))  # Reduce size
    return img

# Loading training dataset
def train_data_load(img_rows=240, img_cols=240, color_type=1):
    train_images = []
    train_labels = []

    # Loop over the training folder
    for classes in tqdm(range(10)):
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

x_train, x_test, y_train, y_test = read_and_normalize_train_data(img_rows, img_cols, 1)

def main_block(x, filters, n, strides, dropout):
    # Normal part
    x_res = Conv2D(filters, (3, 3), strides=strides, padding="same")(x)  # , kernel_regularizer=l2(5e-4)
    x_res = BatchNormalization()(x_res)
    x_res = Activation('relu')(x_res)
    x_res = Conv2D(filters, (3, 3), padding="same")(x_res)
    # Alternative branch
    x = Conv2D(filters, (1, 1), strides=strides)(x)
    # Merge Branches
    x = Add()([x_res, x])

    for i in range(n - 1):
        # Residual conection
        x_res = BatchNormalization()(x)
        x_res = Activation('relu')(x_res)
        x_res = Conv2D(filters, (3, 3), padding="same")(x_res)
        # Apply dropout if given
        if dropout: x_res = Dropout(dropout)(x)
        # Second part
        x_res = BatchNormalization()(x_res)
        x_res = Activation('relu')(x_res)
        x_res = Conv2D(filters, (3, 3), padding="same")(x_res)
        # Merge branches
        x = Add()([x, x_res])

    # Inter block part
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    return x


def build_model(input_dims, output_dim, n, k, act="relu", dropout=None):
    """ Builds the model. Params:
            - n: number of layers. WRNs are of the form WRN-N-K
                 It must satisfy that (N-4)%6 = 0
            - k: Widening factor. WRNs are of the form WRN-N-K
                 It must satisfy that K%2 = 0
            - input_dims: input dimensions for the model
            - output_dim: output dimensions for the model
            - dropout: dropout rate - default=0 (not recomended >0.3)
            - act: activation function - default=relu. Build your custom
                   one with keras.backend (ex: swish, e-swish)
    """
    # Ensure n & k are correct
    assert (n - 4) % 6 == 0
    assert k % 2 == 0
    n = (n - 4) // 6
    # This returns a tensor input to the model
    inputs = Input(shape=(input_dims))

    # Head of the model
    x = Conv2D(16, (3, 3), padding="same")(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    # 3 Blocks (normal-residual)
    x = main_block(x, 16 * k, n, (1, 1), dropout)  # 0
    x = main_block(x, 32 * k, n, (2, 2), dropout)  # 1
    x = main_block(x, 64 * k, n, (2, 2), dropout)  # 2

    # Final part of the model
    x = AveragePooling2D((8, 8))(x)
    x = Flatten()(x)
    outputs = Dense(output_dim, activation="softmax")(x)

    model = Model(inputs=inputs, outputs=outputs)
    return model

x_train[0].shape

#model = vgg_std16_model(img_rows=img_rows, img_cols=img_cols)
model = build_model((224,224,1), 10,16,4)
# model.load_weights('../input/weights/weights.h5')
model.compile("adam","categorical_crossentropy", ['accuracy'])

model.summary()

model.evaluate(x_test, y_test)

model.fit(x_train, y_train, batch_size=40, epochs=10, validation_data=(x_test, y_test))

model.evaluate(x_test, y_test)

model.save('saved_model/model_kaggle_v2.keras')