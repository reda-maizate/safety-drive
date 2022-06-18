import urllib
from typing import List, Tuple
import boto3
import cv2
import logging
import numpy as np
import keras
import config as conf

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

s3 = boto3.client("s3")


def lambda_handler(event, context) -> None:
    url = preprocess(event)
    process(url)


def parse_event(event) -> Tuple[str, str, str]:
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    user_id = key.split('_')[-1].split('.')[0]
    return bucket, key, user_id


def preprocess(event) -> str:
    LOGGER.info(f"started preprocessing")
    (key, bucket, user_id) = parse_event(event)
    LOGGER.info(f"found new video input from {bucket}/{key} for the user_id {user_id}")
    url = s3.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": bucket, "Key": key}
    )
    return url


def process(url: str) -> None:
    # Turn videos into frames
    LOGGER.info(f"started turning videos into frames")
    frames = turn_video_into_frames(url)
    # Predict the frames with our model
    LOGGER.info(f"started predicting frames")
    scores, predictions_labels = predict(frames)
    # Post-process the predictions to match the RDS database
    LOGGER.info(f"started post-processing predictions")
    # post_process(scores, predictions_labels)
    LOGGER.info(f"finished processing")


def turn_video_into_frames(url: str) -> np.ndarray:
    video = cv2.VideoCapture(url)
    index = 0
    frames = []

    while video.isOpened():
        ret, frame = video.read()

        if frame is not None:
            if index % conf.FRAME_RATE == 0:
                colored_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                resized_frame = cv2.resize(colored_frame, conf.IMG_SIZE)
                resized_frame = resized_frame[np.newaxis, ...]
                frames.append(resized_frame)
        else:
            break

        index += 1

    frames = np.vstack(frames)
    return frames


def predict(frames: np.ndarray) -> Tuple[List[List[float]], List[str]]:
    model = keras.models.load_model("base_model_ep_47_val_acc_0.99.h5")
    scores = model.predict(frames)
    predictions_labels = [conf.LABELS[np.argmax(score)] for score in scores]
    LOGGER.info(f"predictions_labels: {predictions_labels}")
    return scores, predictions_labels


# def post_process(scores: List[List[float]], predictions_labels: List[str]):
#     ...
