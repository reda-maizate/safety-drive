################ Lambda ################

# Create the Lambda IAM resource
resource "aws_iam_role" "lambda_iam" {
  name = var.lambda_role_name
  assume_role_policy = data.aws_iam_policy_document.policy_lambda_iam.json
}

# Create the Lambda function
resource "aws_lambda_function" "process_lambda" {
  depends_on       = [
                      null_resource.ecr_image
                     ]
  function_name    = var.function_name_pipeline
  role             = aws_iam_role.lambda_iam.arn
  image_uri        = "${aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.lambda_image.id}"
  package_type     = "Image"
  memory_size      = "1024"
  timeout          = "300"

  environment {
    variables = {
      RDS_ENDPOINT = var.rds_endpoint
      RDS_USERNAME = var.rds_username
      RDS_PASSWORD = var.rds_password
    }
  }

}

# Create the trigger from the S3 bucket to the Lambda function
resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  bucket = var.s3_bucket_id
  lambda_function {
    lambda_function_arn = aws_lambda_function.process_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".avi"
  }
}

# Create the Lambda function permissions
resource "aws_lambda_permission" "process-permission" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.process_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${var.s3_bucket_id}"
}

# Create an IAM Role for the S3 function
resource "aws_iam_role_policy" "revoke_keys_role_policy" {
  name = var.lambda_iam_policy_name_pipeline
  role = aws_iam_role.lambda_iam.id

  policy = data.aws_iam_policy_document.policy_s3.json
}