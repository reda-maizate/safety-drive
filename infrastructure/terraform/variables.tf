# Create variables

variable "aws_account_id" {
  default = ""
}

variable "region" {
  description = "GCP Region"
  default = ""
}

variable "function_name" {
  default = ""
}

variable "lambda_role_name" {
  default = ""
}

variable "lambda_iam_policy_name" {
  default = ""
}

variable "bucket_name" {
  default = ""
}

variable "ecr_repository_name" {
  default = ""
}

variable "profile_name" {
  default = ""
}