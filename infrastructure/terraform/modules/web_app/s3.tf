data "archive_file" "website" {
  type = "zip"
  source_dir = "../../../src/web_app"
  output_path = "../../../src/web_app.zip"
}


resource "aws_s3_object" "website" {
  depends_on = [
    data.archive_file.website
  ]
  bucket = var.s3_bucket_name
  key    = "website.zip"
  source = data.archive_file.website.output_path

  etag = filemd5(data.archive_file.website.output_path)
}