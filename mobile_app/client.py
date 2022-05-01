import hashlib
import hmac
import os
import time
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import boto3

from mobile_app.kinesis import KinesisVideoStream

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
