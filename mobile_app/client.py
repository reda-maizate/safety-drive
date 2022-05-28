from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from mobile_app.services.video_camera import capture_webcam_video

Builder.load_file("templates/index.kv")


class SafetyDriveApp(BoxLayout):
    def play(self):
        """
        Function to start/stop the camera
        """
        camera = self.ids["camera"]
        camera.play = not camera.play
        print("Started")

    @staticmethod
    def send_video_to_s3():
        """
        Function to send data to S3.
        """
        capture_webcam_video("camera_video")


class Main(App):
    def build(self):
        return SafetyDriveApp()


Main().run()
