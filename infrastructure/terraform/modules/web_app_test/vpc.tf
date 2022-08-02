resource "aws_vpc" "my-vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "my-vpc"
  }
}

resource "aws_internet_gateway" "internet-gw" {
  vpc_id = aws_vpc.my-vpc.id
  tags = {
    Name = "internet-gw"
  }
}

data "aws_availability_zones" "AZ" {
  state = "available"
}

resource "aws_subnet" "subnets-public" {
  count = 3
  vpc_id                  = aws_vpc.my-vpc.id
  cidr_block              = "10.0.${length(data.aws_availability_zones.AZ.names) + count.index}.0/24"
  map_public_ip_on_launch = true
  availability_zone = element(data.aws_availability_zones.AZ.names, count.index)
  tags = {
    Name = "subnet-public-${element(data.aws_availability_zones.AZ.names, count.index)}"
  }
}