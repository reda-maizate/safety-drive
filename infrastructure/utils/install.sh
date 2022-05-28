#!/bin/bash
# Author: Réda MAIZATE
# Date: 28/05/2022

# Define variables
AWS_ACCESS_KEY_ID=$1
AWS_SECRET_ACCESS_KEY=$2
AWS_DEFAULT_REGION=$3
AWS_BUCKET=$4

# Install required packages and create the package
mkdir python
#cp src/*.py python/
pip3.8 install opencv-python-headless -t python/
pip3.8 install opencv-python -t python/
zip -r layer.zip python

# Install AWS CLI
apt-get install awscli -y

# Authenticate with AWS
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set default.region $AWS_DEFAULT_REGION

# Upload the layer.zip to AWS S3
aws s3 cp layer.zip s3://"$AWS_BUCKET"/layer.zip \
  && echo "Successfully uploaded file to S3" || (echo "Failed uploaded file to S3" && exit 1)

# Create the layer containing the dependencies of the lambda function
layer_version_arn=$(aws lambda publish-layer-version --layer-name "process_dependencies" \
  --content S3Bucket="$AWS_BUCKET",S3Key=layer.zip \
  --compatible-runtimes python3.8 \
  --compatible-architectures "x86_64" \
  --query LayerVersionArn --output text) \
  && echo "Lambda layer creation completed successfully" || (echo "Failed layer creation" && exit 1)

# Update the lambda function to use the layer
aws lambda update-function-configuration --function-name "Process" \
  --layers "$layer_version_arn" \
  && echo "Lambda function updated successfully" || (echo "Failed to update the lambda function" && exit 1)