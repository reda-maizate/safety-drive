################ Cloudwatch Events ################

# Create a Cloudwatch Log Group to get the logs of the lambda function
resource "aws_cloudwatch_log_group" "process_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.process_lambda.function_name}"
  retention_in_days = 7
  lifecycle {
    prevent_destroy = false
  }
}

#resource "aws_cloudwatch_log_group" "process_log_group_serverless" {
#  name              = "/aws/lambda/${aws_lambda_function.lambda_serverless.function_name}"
#  retention_in_days = 7
#  lifecycle {
#    prevent_destroy = false
#  }
#}


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

resource "aws_iam_role_policy_attachment" "logging_policy_attachment_serverless" {
  role = aws_iam_role.lambda_iam_serverless.id
  policy_arn = aws_iam_policy.process_logging_policy.arn
}