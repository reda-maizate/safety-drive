#resource "aws_cloudwatch_log_group" "process_log_group_serverless" {
#  name              = "/aws/lambda/${aws_lambda_function.lambda_web_app.function_name}"
#  retention_in_days = 7
#  lifecycle {
#    prevent_destroy = false
#  }
#}