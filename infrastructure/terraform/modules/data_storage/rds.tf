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
    cidr_blocks      = ["0.0.0.0/0"]
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

resource "aws_db_instance" "DB" {
  engine = "mysql"
  engine_version = "8.0.27"
  username = "safetyDriveAdmin"
  password = "safety-drive"
  instance_class = "db.t2.micro"
  allocated_storage = 20
  max_allocated_storage = 100
  identifier = "rds-safety-drive"
  vpc_security_group_ids = [aws_security_group.Security-Group-RDS.id] # Non sécurisé, dans le cadre professionnel
  skip_final_snapshot = true
  publicly_accessible = true

  provisioner "local-exec" {
    command = <<EOF
                  pip install pymysql
                  python ../script_create_db.py ${self.endpoint} ${self.username} ${self.password}
              EOF
    interpreter = var.os == "win" ? ["PowerShell", "-Command"] : []
  }
}

resource "aws_rds_cluster" "test_db" {
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

resource "aws_rds_cluster_instance" "example" {
  identifier = "aurora-instance-safety-drive"
  cluster_identifier = aws_rds_cluster.test_db.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.test_db.engine
  engine_version     = aws_rds_cluster.test_db.engine_version
}