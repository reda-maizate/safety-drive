locals {
  ecr_image_tag_web_app = "web_app_image"
  account_id = var.current_account_id
}

resource null_resource ecr_image_web_app {
#  depends_on  = [aws_ecr_repository.repo]
  triggers    = {
    python_file = md5(file("../src/web_app/lambda_web_app.py"))
    docker_file = md5(file("../Dockerfile.web_app"))
 }
 provisioner "local-exec" {
   command = <<EOF
           docker logout ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           docker login --username ${var.token_user_name} --password ${var.token_password} ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           cd ..
           docker build -t ${var.repository_url}:${local.ecr_image_tag_web_app} -f Dockerfile.web_app .
           docker push ${var.repository_url}:${local.ecr_image_tag_web_app}
       EOF
   interpreter = var.os == "win" ? ["PowerShell", "-Command"] : []
 }
}

data aws_ecr_image lambda_image_web_app {
 depends_on = [
   null_resource.ecr_image_web_app
 ]
 repository_name = var.ecr_repository_name
 image_tag       = local.ecr_image_tag_web_app
}
