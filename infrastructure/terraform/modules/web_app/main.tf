data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "subnet_lambda" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_security_groups" "security_group_lambda" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}