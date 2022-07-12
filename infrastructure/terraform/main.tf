
module "data_storage" {
  source = "./modules/data_storage"
  bucket_name = var.bucket_name
  os = var.os
}

module "pipeline_mobile_app_data" {
  depends_on = [
    module.data_storage
  ]
  source = "./modules/pipeline_mobile_app_data"
  region = var.region
  ecr_repository_name = var.ecr_repository_name
  lambda_role_name = var.lambda_role_name
  os = var.os
  function_name_pipeline = var.function_name_pipeline
  lambda_iam_policy_name_pipeline = var.lambda_iam_policy_name_pipeline
  s3_bucket_id = module.data_storage.s3_bucket_id
}

module "web_app" {
  depends_on = [
    module.pipeline_mobile_app_data
  ]
  source = "./modules/web_app"
  region = var.region
  ecr_repository_name = var.ecr_repository_name
  os = var.os
  function_name_web_app = var.function_name_web_app
  api_gateway_name = var.api_gateway_name
  current_account_id = module.pipeline_mobile_app_data.current_account_id
  token_user_name = module.pipeline_mobile_app_data.token_user_name
  token_password = module.pipeline_mobile_app_data.token_password
  repository_url = module.pipeline_mobile_app_data.repository_url
  lambda_iam_name = module.pipeline_mobile_app_data.lambda_iam_name
  lambda_iam_arn = module.pipeline_mobile_app_data.lambda_iam_arn
  db_endpoint = module.data_storage.db_endpoint
  db_username = module.data_storage.db_username
  db_password = module.data_storage.db_password
  vpc_id = module.data_storage.vpc_id
}