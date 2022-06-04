################ Elastic Container Registry ################

data aws_caller_identity current {}

locals {
 account_id          = data.aws_caller_identity.current.account_id
 ecr_repository_name = var.ecr_repository_name
 ecr_image_tag       = "latest"
}

resource aws_ecr_repository repo {
 name = local.ecr_repository_name
}

resource null_resource ecr_image {
 triggers = {
   python_file = md5(file("../src/lambda_function.py"))
   docker_file = md5(file("../Dockerfile"))
 }

 provisioner "local-exec" {
   command = <<EOF
           aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           cd ..
           docker build -t ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag} .
           docker push ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag}
       EOF
 }
}

data aws_ecr_image lambda_image {
 depends_on = [
   null_resource.ecr_image
 ]
 repository_name = local.ecr_repository_name
 image_tag       = local.ecr_image_tag
}
