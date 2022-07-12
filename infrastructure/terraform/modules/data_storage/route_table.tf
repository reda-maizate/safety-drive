resource "aws_route_table" "public-rt" {
  vpc_id = aws_vpc.my-vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet-gw.id
  }
  tags = {
    Name = "route-table-public"
  }
}

resource "aws_route_table_association" "public-rta" {
  count = 3
  route_table_id = aws_route_table.public-rt.id
  subnet_id = element(aws_subnet.subnets-public.*.id, count.index)
}