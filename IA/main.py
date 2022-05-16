import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import cv2
import os
from tqdm import tqdm
from glob import glob
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout,
    BatchNormalization,
    GlobalAveragePooling2D,
)

df = pd.read_csv(
    "C:/Users/Bonjour/Etudes&Travail/Projets/PyCharm/DeepLearningSafetyDrive/Data/driver_imgs_list.csv"
)
print(df.head(5))

# Groupby subjects
by_drivers = df.groupby("subject")
# Group unique drivers
unique_drivers = by_drivers.groups.keys()  # drivers id

print("There are : ", len(unique_drivers), " unique drivers")
print(
    "There is a mean of ",
    round(df.groupby("subject").count()["classname"].mean()),
    " images by driver.",
)

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
        print("Loading directory c{}".format(classes))
        files = glob(
            os.path.join(
                "C:\\Users\\Bonjour\\Etudes&Travail\\Projets\\Pycharm\\DeepLearningSafetyDrive\\Data\\train\\c"
                + str(classes),
                "*.jpg",
            )
        )
        for file in files:
            img = get_image(file, img_rows, img_cols, color_type)
            train_images.append(img)
            train_labels.append(classes)
    return train_images, train_labels


def read_and_normalize_train_data(img_rows, img_cols, color_type):
    X, labels = train_data_load(img_rows, img_cols, color_type)
    y = np_utils.to_categorical(labels, 10)
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    x_train = np.array(x_train, dtype=np.uint8).reshape(
        -1, img_rows, img_cols, color_type
    )
    x_test = np.array(x_test, dtype=np.uint8).reshape(
        -1, img_rows, img_cols, color_type
    )

    return x_train, x_test, y_train, y_test


# Loading validation dataset
def load_test(size=200000, img_rows=64, img_cols=64, color_type=3):
    """
    Same as above but for validation dataset
    """
    path = os.path.join(
        "C:/Users/Bonjour/Etudes&Travail/Projets/PyCharm/DeepLearningSafetyDrive/Data/test",
        "*.jpg",
    )
    files = sorted(glob(path))
    X_test, X_test_id = [], []
    total = 0
    files_size = len(files)
    for file in tqdm(files):
        if total >= size or total >= files_size:
            break
        file_base = os.path.basename(file)
        img = get_image(file, img_rows, img_cols, color_type)
        X_test.append(img)
        X_test_id.append(file_base)
        total += 1
    return X_test, X_test_id


def read_and_normalize_sampled_test_data(size, img_rows, img_cols, color_type=3):
    test_data, test_ids = load_test(size, img_rows, img_cols, color_type)
    test_data = np.array(test_data, dtype=np.uint8)
    test_data = test_data.reshape(-1, img_rows, img_cols, color_type)
    return test_data, test_ids


img_rows = 64
img_cols = 64
color_type = 1
nb_test_samples = 200

# Loading train images
x_train, x_test, y_train, y_test = read_and_normalize_train_data(
    img_rows, img_cols, color_type
)

# Loading validation images
test_files, test_targets = read_and_normalize_sampled_test_data(
    nb_test_samples, img_rows, img_cols, color_type
)

# PART 2

activity_map = {
    "c0": "Safe driving",
    "c1": "Texting - right",
    "c2": "Talking on the phone - right",
    "c3": "Texting - left",
    "c4": "Talking on the phone - left",
    "c5": "Operating the radio",
    "c6": "Drinking",
    "c7": "Reaching behind",
    "c8": "Hair and makeup",
    "c9": "Talking to passenger",
}

plt.figure(figsize=(12, 20))
image_count = 1
BASE_URL = "C:\\Users\\Bonjour\\Etudes&Travail\\Projets\\PyCharm\\DeepLearningSafetyDrive\\Data\\train\\"
for directory in os.listdir(BASE_URL):
    if directory[0] != ".":
        for i, file in enumerate(os.listdir(BASE_URL + directory)):
            if i == 1:
                break
            else:
                fig = plt.subplot(5, 2, image_count)
                image_count += 1
                image = mpimg.imread(BASE_URL + directory + "/" + file)
                plt.imshow(image)
                plt.title(activity_map[directory])

# PART 3

batch_size = 40
n_epochs = 10


def create_model():
    model = Sequential()

    # CNN1
    model.add(
        Conv2D(
            32, (3, 3), activation="relu", input_shape=(img_rows, img_cols, color_type)
        )
    )
    model.add(BatchNormalization())
    model.add(Conv2D(32, (3, 3), activation="relu", padding="same"))
    model.add(BatchNormalization(axis=3))
    model.add(MaxPooling2D(pool_size=(2, 2), padding="same"))
    model.add(Dropout(0.3))

    # CNN2
    model.add(
        Conv2D(
            64, (3, 3), activation="relu", input_shape=(img_rows, img_cols, color_type)
        )
    )
    model.add(BatchNormalization())
    model.add(Conv2D(64, (3, 3), activation="relu", padding="same"))
    model.add(BatchNormalization(axis=3))
    model.add(MaxPooling2D(pool_size=(2, 2), padding="same"))
    model.add(Dropout(0.3))

    # CNN3
    model.add(
        Conv2D(
            128, (3, 3), activation="relu", input_shape=(img_rows, img_cols, color_type)
        )
    )
    model.add(BatchNormalization())
    model.add(Conv2D(128, (3, 3), activation="relu", padding="same"))
    model.add(BatchNormalization(axis=3))
    model.add(MaxPooling2D(pool_size=(2, 2), padding="same"))
    model.add(Dropout(0.3))

    # Output
    model.add(Flatten())
    model.add(Dense(512, activation="relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(128, activation="relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.25))
    model.add(Dense(10, activation="softmax"))

    return model


model = create_model()

# Details about the model
model.summary()

model.compile(
    optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"]
)

history = model.fit(
    x_train,
    y_train,
    validation_data=(x_test, y_test),
    epochs=n_epochs,
    batch_size=batch_size,
    verbose=1,
)

print("History of the training", history.history)


def plot_train_history(history):
    """
    Plot the validation accuracy and validation loss over epochs
    """
    # Summarize history for accuracy
    plt.plot(history.history["accuracy"])
    plt.plot(history.history["val_accuracy"])
    plt.title("Model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    plt.legend(["train", "test"], loc="upper left")
    plt.show()

    # Summarize history for loss
    plt.plot(history.history["loss"])
    plt.plot(history.history["val_loss"])
    plt.title("Model loss")
    plt.ylabel("loss")
    plt.xlabel("epoch")
    plt.legend(["train", "test"], loc="upper left")
    plt.show()


plot_train_history(history)


def plot_test_class(model, test_files, image_number, color_type=1):
    """
    Function that tests or model on test images and show the results
    """
    img_brute = test_files[image_number]
    img_brute = cv2.resize(img_brute, (img_rows, img_cols))
    plt.imshow(img_brute, cmap="gray")

    new_img = img_brute.reshape(-1, img_rows, img_cols, color_type)

    y_prediction = model.predict(new_img, batch_size=batch_size, verbose=1)
    print("Y prediction: {}".format(y_prediction))
    print(
        "Predicted: {}".format(activity_map.get("c{}".format(np.argmax(y_prediction))))
    )

    plt.show()


score1 = model.evaluate(x_test, y_test, verbose=1)

print("Loss: ", score1[0])
print("Accuracy: ", score1[1] * 100, " %")

for i in range(10):
    plot_test_class(model, test_files, i)
