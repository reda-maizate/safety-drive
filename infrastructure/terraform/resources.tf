################ S3 ################

# Create the S3 Bucket
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "safety-drive-bucket"
  force_destroy = true
}

# Create the S3 Bucket Policy
resource "aws_s3_bucket_public_access_block" "s3_policy" {
  bucket = aws_s3_bucket.s3_bucket.id
  block_public_acls   = false
  block_public_policy = false
}

# Create an IAM Role for the S3 function
resource "aws_iam_role_policy" "revoke_keys_role_policy" {
  name = var.lambda_iam_policy_name
  role = aws_iam_role.lambda_iam.id

  policy = data.aws_iam_policy_document.policy_s3.json
}

################ Lambda ################

# Create the Lambda IAM resource
resource "aws_iam_role" "lambda_iam" {
  name = var.lambda_role_name
  assume_role_policy = data.aws_iam_policy_document.policy_lambda_iam.json
}

# Create the Lambda function
resource "aws_lambda_function" "process_lambda" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda_iam.arn
  handler          = "src/${var.handler_name}.lambda_handler"
  runtime          = var.runtime
  filename         = "../src.zip"
  source_code_hash = filebase64sha256("../src.zip")
}

# Create the trigger from the S3 bucket to the Lambda function
resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  bucket = aws_s3_bucket.s3_bucket.id
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
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.s3_bucket.id}"
}

################ Cloudwatch Events ################

# Create a Cloudwatch Log Group to get the logs of the lambda function
resource "aws_cloudwatch_log_group" "process_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.process_lambda.function_name}"
  retention_in_days = 7
  lifecycle {
    prevent_destroy = false
  }
}

# Create the IAM Role for the Cloudwatch logs
resource "aws_iam_policy" "process_logging_policy" {
  name   = "function-logging-policy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Action : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect : "Allow",
        Resource : "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Create the IAM Role for the Cloudwatch attachment logs
resource "aws_iam_role_policy_attachment" "function_logging_policy_attachment" {
  role = aws_iam_role.lambda_iam.id
  policy_arn = aws_iam_policy.process_logging_policy.arn
}