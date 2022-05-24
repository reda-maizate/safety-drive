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

#resource "aws_kinesis_video_stream" "kinesis_video_stream" {
#  name                    = "reda-test-video-stream"
#  data_retention_in_hours = 1
#  media_type              = "video/h264"
#}

resource "aws_s3_bucket" "s3_bucket" {
  bucket = "safety-drive-bucket"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "s3_policy" {
  bucket = aws_s3_bucket.s3_bucket.id
  block_public_acls   = false
  block_public_policy = false
}