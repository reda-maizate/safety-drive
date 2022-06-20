#data "archive_file" "lambda-zip" {
#  type        = "zip"
#  source_dir  = "../src"
#  output_path = "lambda.zip"
#}

data "aws_subnets" "subnet_lambda" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_security_groups" "security_group_lambda" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_iam_role" "lambda_iam_serverless" {
  name               = "lambda-iam"
  assume_role_policy = data.aws_iam_policy_document.policy_lambda_iam.json
}

resource "aws_iam_role_policy_attachment" "iam_role_policy_attachment_lambda_vpc_access_execution" {
  role       = aws_iam_role.lambda_iam_serverless.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_lambda_function" "lambda_serverless" {
#  filename         = "lambda.zip"
  function_name    = "lambda-function"
  role             = aws_iam_role.lambda_iam_serverless.arn
  image_uri = "${aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.lambda_image_serverless.id}"
  package_type = "Image"
  architectures = ["arm64"]
#  handler          = "lambda_serverless.lambda_handler"
#  source_code_hash = data.archive_file.lambda-zip.output_base64sha256
#  runtime          = "python3.8"

  vpc_config {
    security_group_ids = data.aws_security_groups.security_group_lambda.ids
    subnet_ids         = data.aws_subnets.subnet_lambda.ids
  }

  environment {
    variables = {
      ENDPOINT = aws_db_instance.DB.endpoint
      MASTER_USERNAME = aws_db_instance.DB.username
      MASTER_PASSWORD = aws_db_instance.DB.password
    }
  }
}

output "test" {
  value = "${aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.lambda_image_serverless.id}"
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