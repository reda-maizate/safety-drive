resource "aws_iam_role_policy_attachment" "iam_role_policy_attachment_lambda_vpc_access_execution" {
  role       = var.lambda_iam_name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_lambda_function" "lambda_web_app" {
  depends_on           = [
                          aws_s3_object.website
                         ]
  function_name        = var.function_name_web_app
  role                 = var.lambda_iam_arn
  s3_bucket            = var.s3_bucket_name
  s3_key               = "website.zip"
  handler              = "web_app.main.handler"
  runtime              = "python3.6"

  vpc_config {
    security_group_ids = data.aws_security_groups.security_group_lambda.ids
    subnet_ids         = data.aws_subnets.subnet_lambda.ids
  }

  environment {
    variables = {
      ENDPOINT = var.db_endpoint
      MASTER_USERNAME = var.db_username
      MASTER_PASSWORD = var.db_password
    }
  }
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_web_app.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.lambda_api.execution_arn}/*/*/*"
}