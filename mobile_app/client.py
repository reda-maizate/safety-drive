from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from mobile_app.services.video_camera import capture_webcam_video

Builder.load_file("index.kv")


class Main(BoxLayout):
    def play(self):
        """
        Function to start/stop the camera
        """
        camera = self.ids["camera"]
        camera.play = not camera.play
        print("Started")

    @staticmethod
    def send_data_to_s3():
        """
        Function to send data to S3
        """
        capture_webcam_video("camera_video")
        print("Data sent to S3")


class TestCamera(App):
    def build(self):
        return Main()


TestCamera().run()
