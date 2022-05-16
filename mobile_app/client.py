from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from mobile_app.kinesis import KinesisVideoStream

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
    def send_data_to_kinesis():
        """
        Function to send data to Kinesis
        """
        kinesis_stream = KinesisVideoStream()
        status_code = kinesis_stream.send_data()
        print("Data sent to Kinesis with status code {}".format(status_code))


class TestCamera(App):
    def build(self):
        return Main()


TestCamera().run()
