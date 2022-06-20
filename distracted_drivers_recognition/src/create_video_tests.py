import cv2
import os
import config as conf
import pandas as pd
import shutil

driver_images_df = pd.read_csv('../input/driver_imgs_list.csv')
driver_images_df["path"] = driver_images_df.apply(lambda x: os.path.join(conf.TRAINING_IMAGES_PATH, x[1], x[2]), axis=1)

video_test_1_images = driver_images_df[(driver_images_df["subject"] == "p002") &
                                       (driver_images_df["classname"] == "c1")]


def put_images_into_directory(images_df, directory):
    for index, row in images_df.iterrows():
        shutil.copy(row["path"], os.path.join(directory, row["img"]))


# put_images_into_directory(video_test_1_images, "test_1")


def create_video_tests(image_folder: str, video_name: str) -> None:
    """
    Creates a video from a folder of images.
    :param image_folder:
    :param video_name:
    :return:
    """
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


create_video_tests('test_1', 'videotest_1.avi')
