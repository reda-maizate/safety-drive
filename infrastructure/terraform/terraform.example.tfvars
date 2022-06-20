# This file is used to configure the Terraform project.

aws_account_id         = "" # Your AWS account ID (e.g., 123456789012)
region                 = "" # Your AWS region (e.g., us-east-1)
function_name_pipeline = "" # The name of the Lambda function (e.g., my-function)
lambda_role_name       = "" # The name of the Lambda IAM role (e.g., lambda-my-role)
lambda_iam_policy_name_pipeline = "" # The name of the Lambda IAM policy (e.g., lambda-my-policy)
bucket_name            = "" # The name of the S3 bucket (e.g., my-bucket)
ecr_repository_name    = "" # The name of the ECR repository (e.g., my-repository)