import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import boto3

Builder.load_string(
    """
<Main>:
    orientation: 'vertical'
    Label:
        text: 'Client'
        font_size: '30sp'
        size_hint_y: '0.1'
    Camera:
        id: camera
        resolution: (1920, 1080)
        play: False
    ToggleButton:
        text: 'Start camera'
        on_press: root.play()
        size_hint_y: None
        height: '48dp'
    ToggleButton:
        text: 'Connect to AWS'
        on_press: root.send_data_to_kinesis()
        size_hint_y: None
        height: '48dp'
    """
)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


class KinesisVideoStream(object):
    def __init__(self, stream):
        self.stream = stream

    def _connected_client(self):
        """
        Connect to Kinesis Video Streams
        """
        return boto3.client(
            "kinesisvideo",
            region_name="us-east-1",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def get_data_endpoint(self):
        """
        Get Data endpoint to send stream video
        """
        client = self._connected_client()
        result = client.get_data_endpoint(StreamName=self.stream, APIName="PUT_MEDIA")
        return result.get("DataEndpoint")


class Main(BoxLayout):
    def play(self):
        """
        Function to start/stop the camera
        """
        camera = self.ids["camera"]
        camera.play = not camera.play
        print("Started")

    def send_data_to_kinesis(self):
        """
        Function to send data to Kinesis
        """
        stream = KinesisVideoStream("reda-test-video-stream")
        # while True:
        data_endpoint = stream.get_data_endpoint()
        print("Data sent to Kinesis")


class TestCamera(App):
    def build(self):
        return Main()


TestCamera().run()
