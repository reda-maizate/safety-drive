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
pip3.8 install opencv-python -t python/
zip -r layer.zip python

# Install AWS CLI
apt-get install awscli -y

# Authenticate with AWS
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set default.region $AWS_DEFAULT_REGION

# Upload the layer.zip to AWS S3
aws s3 cp layer.zip s3://"$AWS_BUCKET"/layer.zip && echo "Successful Upload" || (echo "Failed" && exit 1)

# Update the layer of the lambda function
#aws lambda update-function-code --function-name Process \
#    --s3-bucket "$AWS_BUCKET" --s3-key ${s3_deploy_key} \
#    --publish ${aws_cli_profile} \
#    && echo "Deployment completed successfully" || (echo "Failed" && exit 1)