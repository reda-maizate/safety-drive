data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "Security-Group-RDS" {
  name        = "Security-Group-RDS"
  description = "Allow connection to RDS"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description      = "MySQL"
    from_port        = 3306
    to_port          = 3306
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"] # Non sécurisé, dans le cadre professionnel
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Security-Group-RDS"
  }
}

resource "aws_rds_cluster" "rds-cluster" {
  cluster_identifier = "rds-cluster-safety-drive"
  engine             = "aurora-mysql"
  engine_mode        = "provisioned"
  engine_version     = "8.0.mysql_aurora.3.02.0"
  database_name      = "test_db_1"
  master_username    = "safetyDriveAdmin"
  master_password    = "safety-drive"
  skip_final_snapshot = true
  vpc_security_group_ids = [aws_security_group.Security-Group-RDS.id]

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
                  python ../script_create_db.py ${self.endpoint} ${aws_rds_cluster.rds-cluster.master_username} ${aws_rds_cluster.rds-cluster.master_password}
              EOF
    interpreter = var.os == "win" ? ["PowerShell", "-Command"] : []
  }
}