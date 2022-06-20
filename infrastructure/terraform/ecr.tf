################ Elastic Container Registry ################

data aws_caller_identity current {}

data aws_ecr_authorization_token token {}

resource aws_ecr_repository repo {
 name = var.ecr_repository_name
}

resource null_resource ecr_image {
  depends_on = [aws_ecr_repository.repo]
 triggers = {
   python_file = md5(file("../src/pipeline/lambda_function.py"))
   docker_file = md5(file("../Dockerfile"))
 }
 provisioner "local-exec" {
   #aws ecr get-login-password --region ${var.region} --profile ${var.profile_name} | docker login --username AWS --password-stdin ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
   command = <<EOF
           docker logout ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com
           docker login --username ${data.aws_ecr_authorization_token.token.user_name} --password ${data.aws_ecr_authorization_token.token.password} ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           cd ..
           docker build -t ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag} .
           docker push ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag}
       EOF
   interpreter = var.os == "win" ? ["PowerShell", "-Command"] : []
 }
}

data aws_ecr_image lambda_image {
 depends_on = [
   null_resource.ecr_image
 ]
 repository_name = var.ecr_repository_name
 image_tag       = local.ecr_image_tag
}

################ Elastic Container Registry Serverless ################

resource null_resource ecr_image_serverless {
  depends_on  = [aws_ecr_repository.repo]
  triggers    = {
    python_file = md5(file("../src/serverless/lambda_serverless.py"))
    docker_file = md5(file("../Dockerfile.serverless"))
 }
 provisioner "local-exec" {
   command = <<EOF
           docker logout ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           docker login --username ${data.aws_ecr_authorization_token.token.user_name} --password ${data.aws_ecr_authorization_token.token.password} ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           cd ..
           docker build -t ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag_serverless} -f Dockerfile.serverless .
           docker push ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag_serverless}
       EOF
   interpreter = var.os == "win" ? ["PowerShell", "-Command"] : []
 }
}

data aws_ecr_image lambda_image_serverless {
 depends_on = [
   null_resource.ecr_image_serverless
 ]
 repository_name = var.ecr_repository_name
 image_tag       = local.ecr_image_tag_serverless
}
