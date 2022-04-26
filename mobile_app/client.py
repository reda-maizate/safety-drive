import json
import os
import uuid

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


class KinesisStream(object):
    def __init__(self, stream):
        self.stream = stream

    def _connected_client(self):
        """Connect to Kinesis Streams"""
        return boto3.client(
            "kinesis",
            region_name="us-east-1",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def send_stream(self, data, partition_key=None):
        """
        data: python dict containing your data.
        partition_key:  set it to some fixed value if you want processing order
                        to be preserved when writing successive records.

                        If your kinesis stream has multiple shards, AWS hashes your
                        partition key to decide which shard to send this record to.

                        Ignore if you don't care for processing order
                        or if this stream only has 1 shard.

                        If your kinesis stream is small, it probably only has 1 shard anyway.
        """

        # If no partition key is given, assume random sharding for even shard write load
        if partition_key is None:
            partition_key = str(uuid.uuid4())

        client = self._connected_client()
        return client.put_record(
            StreamName=self.stream, Data=json.dumps(data), PartitionKey=partition_key
        )


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
        data = {"name": "John", "age": 30}
        stream = KinesisStream("reda-test-kinesis")
        while True:
            stream.send_stream(data=data)
            print("Data sent to Kinesis")


class TestCamera(App):
    def build(self):
        return Main()


TestCamera().run()
