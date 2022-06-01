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