terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  profile = "redaprofile"
}

resource "aws_kinesis_video_stream" "kinesis_video_stream" {
  name                    = "reda-test-kinesis-video-stream"
  data_retention_in_hours = 1
  media_type              = "video/h264"
}