output "s3_bucket_id" {
  value = aws_s3_bucket.s3_bucket.id
}

output "db_endpoint" {
  value = aws_rds_cluster_instance.rds-instance.endpoint
}

output "db_username" {
  value = aws_rds_cluster.rds-cluster.master_username
}

output "db_password" {
  value = aws_rds_cluster.rds-cluster.master_password
}