resource "aws_s3_object" "website" {
  bucket = var.s3_bucket_name
  key    = "website.zip"
  source = "${path.cwd}/../src/web_app/web_app.zip"

  etag = filemd5("${path.cwd}/../src/web_app/web_app.zip")
}