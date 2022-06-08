import os.path

# Paths
IMAGES_PATH = "../input/imgs/"
TRAINING_CSV = "../input/driver_imgs_list.csv"
TRAINING_IMAGES_PATH = os.path.join(IMAGES_PATH, "train")
TEST_IMAGES_PATH = os.path.join(IMAGES_PATH, "test")
OUTPUT_PATH = "../models/"
LOG_DIR = "../logs/"

# Hyperparameters
IMG_SIZE = (32, 32)
IMG_CHANNELS = 3
BATCH_SIZE = 256
SEED = 1337

# Helpers
TRAIN_VAL_SPLIT = 0.2
NUM_CLASSES = 10
NUM_EPOCHS = 10
LABELS = {
    0: "safe driving",
    1: "texting - right",
    2: "talking on the phone - right",
    3: "texting - left",
    4: "talking on the phone - left",
    5: "operating the radio",
    6: "drinking",
    7: "reaching behind",
    8: "hair and makeup",
    9: "talking to passenger",
}
