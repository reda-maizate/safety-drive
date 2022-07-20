import os
import urllib
from datetime import datetime
from typing import Tuple, List
import logging
import boto3
import cv2
import numpy as np
import keras
import config as conf
import pymysql


rds_endpoint = os.environ["RDS_ENDPOINT"]
rds_username = os.environ["RDS_USERNAME"]
rds_password = os.environ["RDS_PASSWORD"]
rds_db_name = "safety_drive_db"

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

s3 = boto3.client("s3")


def lambda_handler(event, context) -> None:  # pylint: disable=unused-argument
    """
    Lambda function that is triggered by S3 events.
    :param event:
    :param context:
    :return:
    """
    LOGGER.info("started preprocessing")
    user_id = preprocess(event)
    process(user_id)
    LOGGER.info("finished processing")


def parse_event(event) -> Tuple[str, str, str]:
    """
    Parse the event.
    :param event:
    :return:
    """
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    user_id = key.split("_")[-1].split(".")[0]
    return bucket, key, user_id


def preprocess(event) -> str:
    """
    Preprocess the video.
    :param event:
    :return:
    """
    (bucket, key, user_id) = parse_event(event)
    LOGGER.info(f"found new video input from {bucket}/{key} for the user_id {user_id}")
    s3.download_file(bucket, key, conf.TEMP_FILE)
    return user_id


def process(user_id: str) -> None:
    """
    Process the video.
    :return:
    """
    # Turn videos into frames
    LOGGER.info("started turning videos into frames")
    frames = turn_video_into_frames()
    # Predict the frames with our model
    LOGGER.info("started predicting frames")
    predictions_labels = predict(frames)
    # Post-process the predictions to match the RDS database
    LOGGER.info(f"started post-processing predictions")
    post_process(user_id, predictions_labels)


def turn_video_into_frames() -> np.ndarray:
    """
    Turn the video into frames.
    :return:
    """
    video = cv2.VideoCapture(conf.TEMP_FILE)
    index = 0
    frames = []

    while video.isOpened():
        _, frame = video.read()

        if frame is not None:
            if index % conf.FRAME_RATE == 0:
                colored_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                resized_frame = cv2.resize(colored_frame, conf.IMG_SIZE)
                resized_frame = resized_frame[np.newaxis, ...]
                frames.append(resized_frame)
        else:
            break

        index += 1

    video.release()
    frames = np.vstack(frames)
    return frames


def predict(frames: np.ndarray) -> List[str]:
    """
    Predict the frames with our model.
    :param frames:
    :return:
    """
    model = keras.models.load_model("base_model_ep_47_val_acc_0.99.h5")
    scores = model.predict(frames)
    predictions_labels = [conf.LABELS[np.argmax(score)] for score in scores]
    LOGGER.info(f"predictions_labels: {predictions_labels}")
    return predictions_labels


def post_process(user_id: str, predictions_labels: List[str]):
    try:
        conn = pymysql.connect(
            host=rds_endpoint,
            user=rds_username,
            passwd=rds_password,
            db=rds_db_name,
            connect_timeout=5,
        )
    except pymysql.MySQLError as e:
        LOGGER.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        LOGGER.error(e)

    with conn.cursor() as session:
        for prediction in predictions_labels:
            session.execute(
                "INSERT INTO PREDICTIONS (value, datetime, user) "
                "VALUES (%s, %s, %s)",
                (prediction, datetime.now(), user_id),
            )
        conn.commit()
    LOGGER.info(f"finished post-processing predictions")
