output "current_account_id" {
  value = data.aws_caller_identity.current.id
}

output "token_user_name" {
  value = data.aws_ecr_authorization_token.token.user_name
}

output "token_password" {
  value = data.aws_ecr_authorization_token.token.password
}

output "repository_url" {
  value = aws_ecr_repository.repo.repository_url
}

output "lambda_iam_name" {
  value = aws_iam_role.lambda_iam.name
}

output "lambda_iam_arn" {
  value = aws_iam_role.lambda_iam.arn
}