locals {
 account_id          = data.aws_caller_identity.current.account_id
 ecr_repository_name = var.ecr_repository_name
 ecr_image_tag       = "latest"
}