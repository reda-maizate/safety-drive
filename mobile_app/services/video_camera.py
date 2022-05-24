import cv2

from mobile_app.services.s3 import S3


def get_video_capture(num_of_videos):
    video = cv2.VideoCapture(0)

    if video.isOpened() is False:
        print("Error reading video file")

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    size = (frame_width, frame_height)
    result = cv2.VideoWriter('filename.avi',
                             cv2.VideoWriter_fourcc(*'XVID'),
                             10, size)

    num_frames = 0

    while num_frames < 50:
        ret, frame = video.read()
        result.write(frame)
        cv2.imshow('Frame', frame)
        num_frames += 1
        if num_frames % 10 == 0:
            print(num_frames)

    video.release()
    result.release()

    cv2.destroyAllWindows()
    s3 = S3()
    s3.upload_file(file_path="filename.avi", key=f"camera_video_{num_of_videos + 1}.avi")
    print("The video was sent to S3")
