resource "aws_db_subnet_group" "db-subnets" {
  name = "db-subnets"
  subnet_ids = aws_subnet.subnets-public.*.id
  tags = {
    Name = "DB-subnet-group"
  }
}

resource "aws_rds_cluster" "rds-cluster" {
  cluster_identifier = "rds-cluster-safety-drive"
  engine             = "aurora-mysql"
  engine_mode        = "provisioned"
  engine_version     = "8.0.mysql_aurora.3.02.0"
  database_name      = "db_safety_drive"
  master_username    = "safetyDriveAdmin"
  master_password    = "safety-drive"
  skip_final_snapshot = true
  db_subnet_group_name = aws_db_subnet_group.db-subnets.id
  vpc_security_group_ids = [aws_default_security_group.default_security_group.id]

  serverlessv2_scaling_configuration {
    max_capacity = 1.0
    min_capacity = 0.5
  }
}

resource "aws_rds_cluster_instance" "rds-instance" {
  identifier = "aurora-instance-safety-drive"
  cluster_identifier = aws_rds_cluster.rds-cluster.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.rds-cluster.engine
  engine_version     = aws_rds_cluster.rds-cluster.engine_version
  publicly_accessible = true

  provisioner "local-exec" {
    command = <<EOF
                  pip install pymysql
                  python3 ../script_create_db.py ${self.endpoint} ${aws_rds_cluster.rds-cluster.master_username} ${aws_rds_cluster.rds-cluster.master_password}
              EOF
    interpreter = var.os == "win" ? ["PowerShell", "-Command"] : []
  }
}