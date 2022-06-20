locals {
 account_id               = data.aws_caller_identity.current.account_id
 ecr_image_tag            = "latest"
 ecr_image_tag_serverless = "serverless_image"
}