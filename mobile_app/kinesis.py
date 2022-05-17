import hashlib
import hmac
import os
import time
from datetime import datetime

import boto3
import requests

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
STREAM_NAME = "reda-test-video-stream"


class KinesisVideoStream(object):
    def __init__(self):
        self._client = self._connected_client()

    @staticmethod
    def _connected_client():
        """
        Connect to Kinesis Video Streams
        """
        return boto3.client(
            "kinesisvideo",
            region_name="us-east-1",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def get_endpoint(self):
        """
        Get Kinesis Video Stream Data endpoint
        """
        result = self._client.get_data_endpoint(
            StreamName=STREAM_NAME, APIName="PUT_MEDIA"
        )
        data_endpoint = result.get("DataEndpoint", None)
        if data_endpoint is None:
            raise Exception("endpoint none")
        return data_endpoint

    class VideoStreamData:
        def __init__(self):
            self.data = ""
            local_video_file_name = "../a_futuristic_dream.mkv"
            with open(local_video_file_name, "rb") as f:
                self.data = f.read()
            self.pointer = 0
            self.size = len(self.data)

        def __iter__(self):
            return self

        def __next__(self):
            if self.pointer >= self.size:
                raise StopIteration
            left = self.size - self.pointer
            chunks_size = min(left, 16000)
            self.pointer += chunks_size
            print("Data: chunk size %d" % chunks_size)
            return self.data[self.pointer - chunks_size : self.pointer]

        def next(self):
            return self.__next__()

    class RequestHeaders:
        def __init__(self, endpoint, access_key, secret_key):
            self.endpoint = endpoint
            self.service = "kinesisvideo"
            self.host = self.get_host_from_endpoint(endpoint)
            self.region = self.get_region_from_endpoint(endpoint)
            self.access_key = access_key
            self.secret_key = secret_key
            self.t = datetime.utcnow()
            self.date_stamp = self.t.strftime("%Y%m%d")
            self.amz_date = self.t.strftime("%Y%m%dT%H%M%SZ")
            self.algorithm = "AWS4-HMAC-SHA256"
            self.credential = (
                self.access_key
                + "/"
                + self.date_stamp
                + "/"
                + self.region
                + "/"
                + self.service
                + "/"
                + "aws4_request"
            )
            self.signed_headers = (
                "connection;content-type;host;transfer-encoding;user-agent;x-amz-date;x-amzn"
                + "-fragment-acknowledgment-required;x-amzn-fragment-timecode-type;x-amzn-producer"
                + "-start-timestamp;x-amzn-stream-name"
            )

        @staticmethod
        def get_host_from_endpoint(endpoint):
            """
            Get the host from the endpoint.

            :param endpoint: The endpoint.
            :return: The host.
            """
            host = endpoint[len("https://") :]
            return str(host)

        @staticmethod
        def get_region_from_endpoint(endpoint):
            """
            Get the region from the endpoint.

            :param endpoint: The endpoint.
            :return: The region.
            """
            region = endpoint[len("https://") :].split(".")[2]
            return str(region)

        @staticmethod
        def sign(key, msg):
            """
            Sign the message with the key.

            :param key: The key to sign the message with.
            :param msg: The message to sign.
            :return: The signature.
            """
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        def get_signature_key(self):
            """
            Get the signature key.

            :param self: The KinesisVideoStream object.
            :return: The signature key.
            """
            key_and_date_signature = self.sign(
                ("AWS4" + self.secret_key).encode("utf-8"), self.date_stamp
            )
            region_signature = self.sign(key_and_date_signature, self.region)
            service_signature = self.sign(region_signature, self.service)
            type_request_signature = self.sign(service_signature, "aws4_request")

            canonical_request = (
                "POST"
                + "\n"
                + "/putMedia\n\n"
                + "connection:keep-alive\n"
                + "content-type:application/json\n"
                + "host:"
                + self.host
                + "\n"
                + "transfer-encoding:chunked\n"
                + "user-agent:AWS-SDK-KVS/2.0.2 GCC/7.4.0 Linux/4.15.0-46-generic x86_64\n"
                + "x-amz-date:"
                + self.amz_date
                + "\n"
                + "x-amzn-fragment-acknowledgment-required:1\n"
                + "x-amzn-fragment-timecode-type:ABSOLUTE\n"
                + "x-amzn-producer-start-timestamp:"
                + repr(time.time())
                + "\n"
                + "x-amzn-stream-name:"
                + STREAM_NAME
                + "\n\n"
                + self.signed_headers
                + "\n"
                + hashlib.sha256("".encode("utf-8")).hexdigest()
            )

            string_to_sign = (
                self.algorithm
                + "\n"
                + self.amz_date
                + "\n"
                + self.date_stamp
                + "/"
                + self.region
                + "/"
                + self.service
                + "/aws4_request\n"
                + hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
            )

            signature = hmac.new(
                type_request_signature,
                string_to_sign.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            return signature

        def get_request_parameters(self):
            """
            Get the request parameters.

            :return: The request parameters.
            """

            authorization_header = (
                self.algorithm
                + " "
                + "Credential="
                + self.credential
                + ", "
                + "SignedHeaders="
                + self.signed_headers
                + ", "
                + "Signature="
                + self.get_signature_key()
                + ""
            )

            request_parameters = {
                "Accept": "*/*",
                "Authorization": authorization_header,
                "connection": "keep-alive",
                "content-type": "application/json",
                "transfer-encoding": "chunked",
                "user-agent": "AWS-SDK-KVS/2.0.2 GCC/7.4.0 Linux/4.15.0-46-generic x86_64",
                "x-amz-date": self.t.strftime("%Y%m%dT%H%M%SZ"),
                "x-amzn-fragment-acknowledgment-required": "1",
                "x-amzn-fragment-timecode-type": "ABSOLUTE",
                "x-amzn-producer-start-timestamp": repr(time.time()),
                "x-amzn-stream-name": STREAM_NAME,
                "Expect": "100-continue",
            }
            print(request_parameters)
            return request_parameters

    def send_data(self):
        """
        Send data to Kinesis
        """
        endpoint = self.get_endpoint()
        headers = self.RequestHeaders(
            endpoint, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
        )
        request = requests.post(
            endpoint + "/putMedia",
            data=self.VideoStreamData(),
            headers=headers.get_request_parameters(),
        )
        print(request.text)
        return request.status_code
