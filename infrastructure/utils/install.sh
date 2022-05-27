#!/bin/bash
# Copyright 2022 - Réda MAIZATE

# Define variables
AWS_ACCESS_KEY_ID=$1
AWS_SECRET_ACCESS_KEY=$2
AWS_DEFAULT_REGION=$3
AWS_BUCKET=$4

# Install required packages and create the package
mkdir python
pip3.8 install opencv-python -t python/
zip -r layer.zip python

# Install AWS CLI
apt-get install awscli -y

# Authenticate with AWS
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set default.region $AWS_DEFAULT_REGION

echo "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY" "$AWS_DEFAULT_REGION" "$AWS_BUCKET"

# Upload the layer.zip to AWS S3
aws s3 cp layer.zip s3://"$AWS_BUCKET"/layer.zip