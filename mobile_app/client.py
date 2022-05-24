from time import sleep

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from mobile_app.kinesis import KinesisVideoStream
from mobile_app.services.s3 import S3
from mobile_app.services.video_camera import get_video_capture

Builder.load_file("index.kv")


class Main(BoxLayout):
    def play(self):
        """
        Function to start/stop the camera
        """
        camera = self.ids["camera"]
        camera.play = not camera.play
        print("Started")

    def send_data_to_s3(self):
        """
        Function to send data to S3
        """
        i = 0
        while i < 3:
            get_video_capture(i)
            i += 1
        # print("Data sent to S3")


class TestCamera(App):
    def build(self):
        return Main()


TestCamera().run()
