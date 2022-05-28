import boto3
import cv2
import os

s3 = boto3.client("s3")


def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = "camera_video.avi"

    url = s3.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": bucket, "Key": key}
    )
    process_video_input(url)


def process_video_input(url):
    turn_videos_into_frames(url)


def turn_videos_into_frames(url):
    video = cv2.VideoCapture(url)
    os.makedirs("/tmp/camera_video", exist_ok=True)

    idx = 0
    while video.isOpened():
        ret, frame = video.read()
        cv2.imwrite(f"/tmp/camera_video/{idx}.jpg", frame)
        if idx % 10 == 0:
            print(f"INFO : {idx} number of frames saved")
        idx += 1

    print(os.listdir("."))
