import keras.models
import numpy as np  # linear algebra
import cv2
import os
from tqdm import tqdm
from glob import glob
import matplotlib.pyplot as plt


# Read with opencv
def get_image(path, img_rows, img_cols, color_type=3):
    if color_type == 1:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (img_rows, img_cols))  # Reduce size
    return img


# Loading validation dataset
def load_test(size=200000, img_rows=64, img_cols=64, color_type=3):
    """
    Same as above but for validation dataset
    """
    path = os.path.join('C:/Users/Bonjour/Etudes&Travail/Projets/PyCharm/DeepLearningSafetyDrive/Data/my_test', '*.jpg')
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


img_rows = 128
img_cols = 128
color_type = 1
nb_test_samples = 200

# Loading validation images
test_files, test_targets = read_and_normalize_sampled_test_data(nb_test_samples, img_rows, img_cols, color_type)

activity_map = {'c0': 'Safe driving',
                'c1': 'Texting - right',
                'c2': 'Talking on the phone - right',
                'c3': 'Texting - left',
                'c4': 'Talking on the phone - left',
                'c5': 'Operating the radio',
                'c6': 'Drinking',
                'c7': 'Reaching behind',
                'c8': 'Hair and makeup',
                'c9': 'Talking to passenger'}

batch_size = 40

model = keras.models.load_model(
    "saved_model/cnn/3cnn_32_64_128_neurons_bs40/model_seed_7_2022-05-28_18_12_51.575187.keras")

# Details about the model
model.summary()

for i in range(len(test_files)):
    img_brute = test_files[i]
    img_brute = cv2.resize(img_brute, (img_rows, img_cols))
    plt.imshow(img_brute, cmap='gray')

    new_img = img_brute.reshape(-1, img_rows, img_cols, 1)

    y_prediction = model.predict(new_img, batch_size=batch_size, verbose=1)
    print('Y prediction: {}'.format(y_prediction))
    print('label:', test_targets[i])
    print('Predicted: {}'.format(activity_map.get('c{}'.format(np.argmax(y_prediction)))))

    plt.show()
