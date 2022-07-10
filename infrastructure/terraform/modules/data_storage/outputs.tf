output "s3_bucket_id" {
  value = aws_s3_bucket.s3_bucket.id
}

output "db_endpoint" {
  value = aws_db_instance.DB.endpoint
}

output "db_username" {
  value = aws_db_instance.DB.username
}

output "db_password" {
  value = aws_db_instance.DB.password
}