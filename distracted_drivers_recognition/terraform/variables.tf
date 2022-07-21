variable "aws_account_key_id" {
  description = "The AWS account key ID"
  type        = string
  default     = ""
}

variable "aws_account_secret_key" {
  description = "The AWS account secret key"
  type        = string
  default     = ""
}

variable "region" {
  description = "The AWS region"
  type        = string
  default     = ""
}

variable "profile_name" {
  description = "The AWS profile name"
  type        = string
  default     = ""
}