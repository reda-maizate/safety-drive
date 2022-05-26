import os

import cv2

from mobile_app.services.s3 import S3

NUM_FRAMES_WANTED = 25


def capture_webcam_video(temp_file_name: str) -> None:
    video = cv2.VideoCapture(0)

    if video.isOpened() is False:
        print("Error reading video file")

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    size = (frame_width, frame_height)
    codec = cv2.VideoWriter_fourcc(*'XVID')

    result = cv2.VideoWriter(f'{temp_file_name}.avi',
                             codec,
                             40,
                             size)

    save_video(video, result, NUM_FRAMES_WANTED)
    send_to_s3(temp_file_name, "camera_video")


def send_to_s3(temp_file_name: str, key_name: str) -> None:
    s3 = S3()
    s3.upload_file(file_path=f"{temp_file_name}.avi", key=f"{key_name}.avi")
    os.remove(f"{temp_file_name}.avi")
    print("The video was sent to S3")


def save_video(video: cv2.VideoCapture, video_writer: cv2.VideoWriter, num_of_frames_wanted: int):
    # Option n°1 : Save a video and send it to S3
    for idx in range(1, num_of_frames_wanted + 1):
        ret, frame = video.read()
        video_writer.write(frame)
        if idx % 10 == 0:
            print(f"info : {idx} number of frames saved")

    # Option n°2 : Save all frames in a directory and send it to S3
    # os.makedirs("camera_video", exist_ok=True)

    # for idx in range(num_of_frames_wanted):
    #     ret, frame = video.read()
    #     cv2.imwrite(f"camera_video/{idx}.jpg", frame)
    #     if idx % 10 == 0:
    #         print(f"{idx} number of frames saved")

    video.release()
    video_writer.release()
