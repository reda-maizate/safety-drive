################ Elastic Container Registry ################

data aws_caller_identity current {}

data aws_ecr_authorization_token token {}

resource aws_ecr_repository repo {
 name = local.ecr_repository_name
}

resource null_resource ecr_image {
  depends_on = [aws_ecr_repository.repo]
 triggers = {
   python_file = md5(file("../src/lambda_function.py"))
   docker_file = md5(file("../Dockerfile"))
 }
 provisioner "local-exec" {
   command = <<EOF
           docker logout ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           docker login --username ${data.aws_ecr_authorization_token.token.user_name} --password ${data.aws_ecr_authorization_token.token.password} ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           cd ..
           docker build -t ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag} .
           docker push ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag}
       EOF
   interpreter = ["PowerShell", "-Command"]
 }
}

data aws_ecr_image lambda_image {
 depends_on = [
   null_resource.ecr_image
 ]
 repository_name = local.ecr_repository_name
 image_tag       = local.ecr_image_tag
}

resource null_resource ecr_image_serverless {
  depends_on = [aws_ecr_repository.repo]
 triggers = {
   python_file = md5(file("../src/lambda_serverless.py"))
   docker_file = md5(file("../Dockerfile.serverless"))
 }
 provisioner "local-exec" {
   command = <<EOF
           docker logout ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           docker login --username ${data.aws_ecr_authorization_token.token.user_name} --password ${data.aws_ecr_authorization_token.token.password} ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           cd ..
           docker build -t ${aws_ecr_repository.repo.repository_url}:serverless_image -f Dockerfile.serverless .
           docker push ${aws_ecr_repository.repo.repository_url}:serverless_image
       EOF
   interpreter = ["PowerShell", "-Command"]
 }
}

data aws_ecr_image lambda_image_serverless {
 depends_on = [
   null_resource.ecr_image_serverless
 ]
 repository_name = local.ecr_repository_name
 image_tag       = "serverless_image"
}
