#data "archive_file" "website" {
#  type = "zip"
#  source_dir = "../../../src/web_app"
#  output_path = "../../../src/web_app.zip"
#}

#resource "null_resource" "zip_app_and_dependencies" {
#  provisioner "local-exec" {
#    command = <<EOF
#      cd ../../../src/web_app
#      pip install --target ./package -r ../../requirements-web-app.txt
#      cd package
#      zip -r ../web_app.zip .
#      cd ..
#      zip -g web_app.zip templates
#      zip -g web_app.zip main.py
#      rm -rf package
#    EOF
#  }
#}


resource "aws_s3_object" "website" {
#  depends_on = [
#    null_resource.zip_app_and_dependencies
#  ]
  bucket = var.s3_bucket_name
  key    = "website.zip"
  source = "${path.root}/infrastructure/src/web_app/web_app.zip"

  etag = filemd5("${path.root}/infrastructure/src/web_app/web_app.zip")
}