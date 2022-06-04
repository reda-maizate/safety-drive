import boto3
import cv2
import os
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

s3 = boto3.client("s3")


def lambda_handler(event, context):
    bucket = "safety-drive-bucket"
    key = "camera_video.avi"
    LOGGER.info(f"started processing {bucket}/{key}")
    url = s3.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": bucket, "Key": key}
    )
    LOGGER.info(f"video_camera url is {url}")
    process_video_input(url)
    LOGGER.info(f"finished processing {bucket}/{key}")


def process_video_input(url):
    turn_videos_into_frames(url)


def turn_videos_into_frames(url):
    video = cv2.VideoCapture(url)
    os.makedirs("/tmp/camera_video", exist_ok=True)

    idx = 0
    while video.isOpened():
        ret, frame = video.read()
        cv2.imwrite(f"/tmp/camera_video/{idx}.jpg", frame)
        LOGGER.info(f"{idx} frames processed")
        idx += 1

    LOGGER.info(f"Path : {os.getcwd()}")
    os.chdir("/tmp/camera_video")
    LOGGER.info(f"Path : {os.getcwd()}")

