data "archive_file" "lambda-zip" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "lambda.zip"
}

resource "aws_iam_role" "lambda_iam_serverless" {
  name               = "lambda-iam"
  assume_role_policy = data.aws_iam_policy_document.policy_lambda_iam.json
}

resource "aws_lambda_function" "lambda_serverless" {
  filename         = "lambda.zip"
  function_name    = "lambda-function"
  role             = aws_iam_role.lambda_iam_serverless.arn
  handler          = "lambda_serverless.lambda_handler"
  source_code_hash = data.archive_file.lambda-zip.output_base64sha256
  runtime          = "python3.8"
}

resource "aws_apigatewayv2_api" "lambda_api" {
  name          = "v2-http-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda_stage" {
  api_id      = aws_apigatewayv2_api.lambda_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id               = aws_apigatewayv2_api.lambda_api.id
  integration_type     = "AWS_PROXY"
  integration_method   = "POST"
  integration_uri      = aws_lambda_function.lambda_serverless.invoke_arn
  passthrough_behavior = "WHEN_NO_MATCH"
}

resource "aws_apigatewayv2_route" "lambda_route" {
  api_id    = aws_apigatewayv2_api.lambda_api.id
  route_key = "GET /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_serverless.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.lambda_api.execution_arn}/*/*/*"
}