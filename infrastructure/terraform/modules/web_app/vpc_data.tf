data "aws_subnets" "subnet_lambda" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
}

data "aws_security_groups" "security_group_lambda" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
}